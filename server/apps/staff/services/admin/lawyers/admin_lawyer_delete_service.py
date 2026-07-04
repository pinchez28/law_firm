from apps.common.choices import EmploymentStatus


class AdminLawyerDeleteService:
    """
    Soft-deletes lawyers from admin workflows.
    """

    @staticmethod
    def delete_lawyer(*, lawyer, deleted_by):
        lawyer.is_active = False
        lawyer.employment_status = EmploymentStatus.TERMINATED

        if not lawyer.termination_reason:
            lawyer.termination_reason = "Deleted by administrator."

        lawyer.save()

        return lawyer