import unittest
import requests

class ApiTest(unittest.TestCase):
    """
    Unittest for World Class Government API

    Author: Metaras Charoenseang
    """

    def setUp(self) -> None:
        """
        Set up for test
        """
        self.URL = "https://wcg-apis.herokuapp.com"

        # create citizen for test
        params = self.create_path("1110000000111", "Minerva", "M.", "2/12/1998", "student", "KU")
        requests.post(self.URL + f"/registration?{params}")

    def create_path(self, citizen_id, name, surname, birth_date, occupation, address):
        """
        Create citizen to add to the database
        :parameter
            citizen_id: id of the citizen
            name: citizen name
            surname: citizen surname
            birth_date: citizen birth date
            occupation: citizen occupation
            address: citizen address
        :return
            part of url that contain the parameter.
        """
        return f"citizen_id={citizen_id}&name={name}&surname={surname}&birth_date={birth_date}" \
               f"&occupation={occupation}&address={address}"

    def test_add_citizen(self):
        """
        The valid citizen should valid to registered.

        status code should be 200
        """
        params = self.create_path("1119876543111", "hermione", "Granger", "2/11/1996", "student", "Hogwarts")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual(200, response.status_code)

    # citizen id
    def test_invalid_citizen_id(self):
        """
        Invalid citizen id could not add to the database.
        """
        params = self.create_path("citizen id", "Harry", "Potter", "3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid citizen ID", response.json()["feedback"])

    def test_negative_negative_citizen_id(self):
        """
        Negative citizen id could not add to the database.
        """
        params = self.create_path("-111111111111", "Harry", "Potter", "3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid citizen ID", response.json()["feedback"])

    def test_negative_empty_citizen_id(self):
        """
        Empty citizen id should be invalid.
        """
        params = self.create_path("", "Harry", "Potter", "3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    # name/surname
    def test_empty_name(self):
        """
        Empty citizen name should be invalid.
        """
        params = self.create_path("1111120947111", "", "Potter", "3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_empty_surname(self):
        """
        Empty citizen surname should be invalid.
        """
        params = self.create_path("1111173841111", "Harry", "", "3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_invalid_name(self):
        """
        Invalid citizen name should be invalid.
        """
        params = self.create_path("1111198274111", "1234", "Potter", "3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid name datatype", response.json()["feedback"])

    def test_invalid_surname(self):
        """
        Invalid citizen surname should be invalid.
        """
        params = self.create_path("1111204819111", "Harry", "1234", "3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid surname datatype", response.json()["feedback"])

    # birth date
    def test_invalid_birthdate(self):
        """
        Invalid citizen birth date should be invalid.
        """
        params = self.create_path("1111112411840", "Draco", "Malfoy", "-3/4/2001", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid birth date format", response.json()["feedback"])

    def test_empty_birthdate(self):
        """
        Empty citizen birth date should be invalid.
        """
        params = self.create_path("1111048294111", "Harry", "Potter", "", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_too_young_citizen(self):
        """
        Citizen should be older than 12 years old.
        """
        params = self.create_path("1110472842111", "Harry", "Potter", "3/4/2020", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: not archived minimum age", response.json()["feedback"])

    def test_too_old_citizen(self):
        """
        Citizen should be alive.
        """
        params = self.create_path("1111028472911", "Harry", "Potter", "3/4/1820", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid birth date", response.json()["feedback"])

    # occupation
    def test_empty_occupation(self):
        """
        Empty citizen occupation should be invalid.
        """
        params = self.create_path("1111111111111", "Harry", "Potter", "3/4/2001", "", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_invalid_occupation(self):
        """
        Invalid citizen occupation should be invalid.
        """
        params = self.create_path("1111294027111", "Harry", "Potter", "3/4/2001", "1", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid occupation datatype", response.json()["feedback"])

    # address
    def test_empty_address(self):
        """
        Empty citizen address should be invalid.
        """
        params = self.create_path("1111102847211", "Harry", "", "3/4/2001", "student", "")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_invalid_address(self):
        """
        Invalid citizen address should be invalid.
        """
        params = self.create_path("1112974824111", "Harry", "Potter", "3/4/2001", "student", "123")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: invalid address datatype", response.json()["feedback"])

    def test_already_registered(self):
        """
        Empty citizen occupation should be invalid.
        """
        params = self.create_path("1110000000111", "Minerva", "M.", "2/12/1998", "student", "KU")
        response = requests.post(self.URL + f"/registration?{params}")
        self.assertEqual("registration failed: this person already registered",
                         response.json()['feedback'])

    def test_delete_citizen_status(self):
        """
        Try to delete the citizen.
        """
        response = requests.delete(self.URL + '/citizen')
        self.assertEqual(200, response.status_code)

    def test_delete_citizen(self):
        """
        Try to delete the citizen.
        """
        requests.delete(self.URL + '/citizen')
        response = requests.get(self.URL + "/registration")
        self.assertNotEqual(0, len(response.json()))

    def test_get_method_for_registration(self):
        """
        Should be about to get the citizen information.
        """
        response = requests.get(self.URL + '/registration')
        self.assertEqual(200, response.status_code)

    def test_get_user_information(self):
        """
        Should be about to get the citizen information.
        """
        citizen_id = "1110000000111"
        endpoint = self.URL + f"/citizen/{citizen_id}"
        response = requests.get(endpoint)
        self.assertEqual("1110000000111", response.json()["citizen-id"])



if __name__ == '__main__':
    unittest.main()