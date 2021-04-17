import json
import os
from dataclasses import asdict
from datetime import datetime
from itertools import count
from pathlib import Path
from typing import Dict, List

import requests
from dacite import from_dict, Config

from constants import GITHUB_TOKEN
from models import RepositoryInfo

current_path = os.path.dirname(os.path.realpath(__file__))


def retrieve_repositories() -> Dict:
    repositories_info: Dict = _read_local()

    if _should_refresh_repos(repositories_info) or not repositories_info:
        repositories_retrieved: List[RepositoryInfo] = _get_all_repositories()
        return _write_local(repositories_retrieved)

    return repositories_info


def _read_local() -> Dict:
    try:
        with open(Path(current_path).joinpath("latest_data.json")) as github_data:
            return json.loads(github_data.read())
    except FileNotFoundError:
        return {}


def _write_local(repositories: List[RepositoryInfo]) -> Dict:
    repositories_info: Dict = {
        "count": len(repositories),
        "updated_at": datetime.now().isoformat(),
        "repos": [asdict(condensed_repo) for condensed_repo in repositories],
    }

    try:
        with open(Path(current_path).joinpath("latest_data.json"), "w") as github_data:
            json.dump(repositories_info, github_data)
    except FileNotFoundError:
        return {}

    return repositories_info


def _should_refresh_repos(local_data: Dict) -> bool:
    if updated_time := local_data.get("updated_at"):
        now_datetime: datetime = datetime.now()
        updated_datetime: datetime = datetime.fromisoformat(updated_time)
        time_difference = now_datetime - updated_datetime

        if time_difference.days >= 1:
            # If the updated time and current time difference is at least 1 day then we refresh the data
            return True
    return False


def _get_all_repositories() -> List[RepositoryInfo]:
    base_url: str = "https://api.github.com/search/repositories"
    repository_infos: List[RepositoryInfo] = []
    for index in count(1):
        url: str = (
            f"{base_url}?q=stars:>1000&good-first-issues:>5&page={index}&per_page=200"
        )
        headers: Dict = {"headers": f"token {GITHUB_TOKEN}"}
        try:
            response: requests.Response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception:
            return repository_infos
        retrieved_repositories: List[Dict] = response.json().get("items", [])

        repository_infos.extend(
            [
                from_dict(RepositoryInfo, repository, config=Config(check_types=False))
                for repository in retrieved_repositories
            ]
        )

    return repository_infos
