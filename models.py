from dataclasses import dataclass


@dataclass
class RepositoryInfo:
    name: str = ""
    html_url: str = ""
    language: str = ""
    updated_at: str = ""
    description: str = ""
    watchers_count: int = 0
    stargazers_count: int = 0
    open_issues_count: int = 0
