from datetime import datetime


class BillParser:
    """Parse Rada bill data to simplify creation of a new Bill object."""

    def parse(self, data):
        """Parse bill data from Rada bill item."""

        phase_date = datetime.strptime(data['currentPhase']['date'],
                                       '%d.%m.%Y').date()
        agenda = data.get('agenda', None)
        parsed_authors = self.parse_initiators(data.get('authors', None))
        parsed_initiators = self.parse_initiators(data.get('initiators', None))
        parsed_executives = self.parse_executives(data.get('executives', None))
        parsed_main_executives = self.parse_main_executives(
            data.get('mainExecutives', None))
        parsed_documents = self.parse_documents(data.get('documents', None))
        parsed_committees = self.prepare_committees(data.get('workOuts', None))
        parsed_bind_bills = self.parse_bills(
            data.get('bind', None))
        parsed_alternatives = self.parse_bills(
            data.get('alternative', None))

        parsed_data = {
            'title': self.none_to_str(data['title']),
            'bill_id': data['id'],
            'number': data['number'],
            'convocation': self.none_to_str(data['registrationConvocation']),
            'session': self.none_to_str(data['registrationSession']),
            'rubric': self.none_to_str(data['rubric']),
            'subject': self.none_to_str(data['subject']),
            'bill_type': self.none_to_str(data['type']),
            'phase': self.none_to_str(data['currentPhase']['title']),
            'phase_date': phase_date,
            'uri': self.none_to_str(data['uri']),
            'registration_date': data['registrationDate'],
            'chronology': data['passings'],
            'agenda': agenda,
            'documents': parsed_documents,
            'committees': parsed_committees,
            'authors': parsed_authors,
            'initiators': parsed_initiators,
            'executives': parsed_executives,
            'main_executives': parsed_main_executives,
            'bind_bills': parsed_bind_bills,
            'alternatives': parsed_alternatives
            }

        return parsed_data

    def parse_initiators(self, initiators):
        """Parse authors from Rada bill item."""

        parsed_initiators = []
        if initiators:
            data = self.parse_root(initiators)
            for person in data:
                if 'official' in person:
                    data = person['official']
                elif 'outer' in person:
                    data = person['outer']
                parsed_person = {
                            'person_id': data['person'].get('id', None),
                            'first_name': self.none_to_str(
                                data['person']['firstname']),
                            'middle_name': self.none_to_str(
                                data['person']['patronymic']),
                            'last_name': data['person']['surname'],
                            'post': self.none_to_str(data.get('post', '')),
                            'organization': self.none_to_str(
                                data.get('organization', '')),
                            'committees_by_title': self.none_to_str(
                                data.get('department', '')),
                            'convocation_by_latin_number': self.none_to_str(
                                data.get('convocation', ''))
                        }
                parsed_initiators.append(parsed_person)

        return parsed_initiators

    def parse_executives(self, initiators):
        """Parse executives from Rada bill item."""

        parsed_initiators = []
        if initiators:
            data = self.parse_root(initiators)
            for person in data:
                parsed_person = {
                        'person_id': person['person']['id'],
                        'first_name': person['person']['firstname'],
                        'middle_name': person['person']['patronymic'],
                        'last_name': person['person']['surname'],
                        'committees_by_title': person.get('department', ''),
                        }
                parsed_initiators.append(parsed_person)

        return parsed_initiators

    def parse_main_executives(self, person):
        """Parse main executives from Rada bill item."""

        parsed_data = []
        if person:
            if not person['executive']['person']['id'] == '':
                parsed_person = {
                    'person_id': person['executive']['person']['id'],
                    'first_name': person['executive']['person']['firstname'],
                    'middle_name': person['executive']['person']['patronymic'],
                    'last_name': person['executive']['person']['surname'],
                    'committees_by_title': person['executive'].get(
                        'department', ''),
                }
                parsed_data.append(parsed_person)
        return parsed_data

    def parse_documents(self, documents):
        """Parse documents from Rada bill item."""

        parsed_documents = []
        if documents:
            if 'source' in documents and 'workflow' in documents:
                root_1 = documents['source']['document']
                root_2 = documents['workflow']['document']
                data_1 = self.parse_root(root_1)
                data_2 = self.parse_root(root_2)
                data = data_1 + data_2
            elif 'source' in documents:
                data = self.parse_root(documents['source']['document'])
            elif 'workflow' in documents:
                data = self.parse_root(documents['workflow']['document'])

            for document in data:
                parsed_document = {
                        'document_type': document.get('type', ''),
                        'date': document.get('date', None),
                        'uri': document.get('uri', '')
                    }
                parsed_documents.append(parsed_document)
        return parsed_documents

    def prepare_committees(self, committees):
        """Prepare complex committee structure for parse_committes function."""

        parsed_committees = []
        if committees:
            data = self.parse_root(committees)
            for item in data:
                parsed = self.parse_committees(item)
                parsed_committees += parsed
        return parsed_committees

    def parse_committees(self, committees):
        """Parse committes from Rada bill item."""

        parsed_committees = []
        if committees:
            data = self.parse_root(committees['workOutCommittees'])
            for committee in data:
                parsed_committee = {
                        'title': committee['title'],
                        'date_got': committee['dateGot'],
                        'date_passed': committee['datePassed']
                    }
                parsed_committees.append(parsed_committee)
        return parsed_committees

    def parse_bills(self, bill_ids):
        """Parse related bill ids from Rada bill item."""

        parsed_bills = []
        if bill_ids:
            data = self.parse_root(bill_ids['refBills'])
            for bill_id in data:
                parsed_bill_id = {
                        'bill_id': bill_id['id']
                    }
                parsed_bills.append(parsed_bill_id)
        return parsed_bills

    def none_to_str(self, value):
        "Convert None to empty string."""

        if value is None:
            return ''
        return value

    def parse_root(self, root):
        """Convert dict root element to list."""

        if type(root) is dict:
            root = [root]
        return root
