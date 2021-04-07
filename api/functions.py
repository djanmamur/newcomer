from dataclasses import asdict
from functools import lru_cache
from itertools import count
from typing import Dict, List

import requests
from dacite import from_dict, Config

from constants import GITHUB_TOKEN
from models import RepositoryInfo


@lru_cache(maxsize=1024)
def retrieve_repos() -> Dict:
    repositories: List[RepositoryInfo] = _get_all_repositories()
    return {
        "count": len(repositories),
        "repos": [asdict(condensed_repo) for condensed_repo in repositories],
    }


def _get_all_repositories() -> List[RepositoryInfo]:
    base_url: str = "https://api.github.com/search/repositories"
    repositoryInfos: List[RepositoryInfo] = []
    for index in count(1):
        url: str = f"{base_url}?q=stars:>1000&good-first-issues:>5&page={index}&per_page=200"
        try:
            repositoryInfos.extend(_get_repositories(url))
        except Exception:
            return repositoryInfos
    return repositoryInfos


def _get_repositories(url: str) -> List[RepositoryInfo]:
    headers: Dict = {"headers": f"token {GITHUB_TOKEN}"}

    response: requests.Response = requests.get(url, headers=headers)
    response.raise_for_status()
    retrieved_repositories: List[Dict] = response.json().get("items", [])

    return [
        from_dict(RepositoryInfo, repository, config=Config(check_types=False))
        for repository in retrieved_repositories
    ]