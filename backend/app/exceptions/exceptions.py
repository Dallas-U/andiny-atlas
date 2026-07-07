class CaseNotFoundException(Exception):
    """Raised when a requested investigation case cannot be found."""

    def __init__(self, case_id: str):

        self.case_id = case_id

        super().__init__(f"Case '{case_id}' was not found.")
