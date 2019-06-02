# -*- coding:utf-8 -*-

from two_step_verification.two_step_verification import TwoStepVerification


class ConsoleVerification(TwoStepVerification):

    def get_verification_type(self, choices):
        if len(choices) > 1:
            possible_values = {}
            print('Select where to send security code')
            for choice in choices:
                print(choice['label'] + ' - ' + choice['value'])
                possible_values[choice['value']] = True
            selected_choice = None
            while selected_choice not in possible_values:
                if selected_choice:
                    print('Wrong choice. Try again')
                selected_choice = input('Your choice: ').strip()
        else:
            print('Message with security code sent to: ' + choices[0]['label'])
            selected_choice = choices[0]['value']

        return selected_choice

    def get_security_code(self):
        security_code = ''
        while len(security_code) != 6 and not isinstance(security_code, int):
            if security_code:
                print('Wrong security code')
            security_code = input('Enter security code:').strip()
        return security_code
