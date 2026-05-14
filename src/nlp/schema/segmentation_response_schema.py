from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class ResumeSegments:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    projects: Optional[str] = None
    certifications: Optional[str] = None
    achievements: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)
