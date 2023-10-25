from enum import Enum
from pythonik.models.base import Response
from pythonik.models.jobs.job_body import JobBody
from pythonik.models.jobs.job_response import JobResponse
from pythonik.specs.base import Spec


CREATE_JOB_PATH = "jobs/"
UPDATE_JOB_PATH = "jobs/{}"


class JobSpec(Spec):
    server = "API/jobs/"

    def create(self, body: JobBody, **kwargs) -> Response:
        """
        Create a job
        """

        resp = self._post(CREATE_JOB_PATH, json=body.model_dump(), **kwargs)

        return self.parse_response(resp, JobResponse)

    def update(self, job_id: str, body: JobBody, **kwargs) -> Response:
        """
        update a job
        """

        resp = self._put(
            UPDATE_JOB_PATH.format(job_id), json=body.model_dump(), **kwargs
        )

        return self.parse_response(resp, JobResponse)
