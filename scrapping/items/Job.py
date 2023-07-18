from dataclasses import dataclass, field


@dataclass
class Job:
    company_name: str = field(default="", metadata={"serializer": str})
    company_about_url: str = field(default="", metadata={"serializer": str})
    location: str = field(default="", metadata={"serializer": str})
    job_title: str = field(default="", metadata={"serializer": str})
    job_url: str = field(default="", metadata={"serializer": str})

    job_type: tuple[str] = '',
    salary: tuple[str] = '',
    shift_and_schedule: tuple[str] = '',
    benefits_and_perks: tuple[str] = '',
