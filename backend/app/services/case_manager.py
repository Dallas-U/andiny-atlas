import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4


class CaseManager:

    def __init__(self):

        self.database = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "data"
            / "investigations.json"
        )

    def save_case(self, customer_name, phone_number, result):

        with open(self.database, "r") as file:
            investigations = json.load(file)

        case = {
            "case_id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "customer_name": customer_name,
            "phone_number": phone_number,
            "result": result
        }

        investigations.append(case)

        with open(self.database, "w") as file:
            json.dump(investigations, file, indent=4)

        return case

    def get_all_cases(self):

        with open(self.database, "r") as file:
            investigations = json.load(file)

        return investigations

    def get_case_by_id(self, case_id):

        investigations = self.get_all_cases()

        for case in investigations:

            if case["case_id"] == case_id:
                return case

        return None

    def search_cases(self, customer_name=None, phone_number=None):

        investigations = self.get_all_cases()

        results = investigations

        if customer_name:

            results = [
                case for case in results
                if case["customer_name"].lower() == customer_name.lower()
            ]

        if phone_number:

            results = [
                case for case in results
                if case["phone_number"] == phone_number
            ]

        return results