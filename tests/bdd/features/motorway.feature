Feature: Validating car details
  Scenario: Successfully obtaining car details
    Given I am on the motorway landing page
    Then enter the number plate
    Then I click value your car
    Then I get the details and comapre against expected