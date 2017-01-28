from pytest_bdd import (
    scenarios,
    given,
    then,
    when,
    parsers,
)
import fixtures

scenarios('.')


def userify(txt):
    return txt


@given('I have ABN credentials at the DCL web interface')
def web_ui():
    return {
        'url': fixtures.DCL_WRITE_DOMAIN,
        'user': fixtures.DCL_TEST_USER,
        'password': fixtures.DCL_TEST_SECRET
    }


@when('I authenticate')
def authenticate(browser, web_ui):
    """I authenticate."""
    browser.visit('{}/openid/openid/SimGuard/'.format(web_ui['url']))
    if 'idp.testpoint.io' in browser.url:
        # we have login page
        browser.fill('login', web_ui['user'])
        browser.fill('password', web_ui['password'])
        # warning: assuming user already have logged in single time with this ABN,
        # so Oauth access confirmation doesn't appear
        button = browser.find_by_xpath('//button[@type="submit"]').first
        button.click()
    else:
        # login worked magically (idp remembers us from previous login)
        pass


@then(parsers.parse("I submit the form"))
def submit_the_form(page_text, browser):
    button = browser.find_by_xpath('//button[@type="submit"]').first
    button.click()


@then(parsers.parse("I see '{page_text:.}'"))
@then(parsers.parse('I see "{page_text:.}"'))
def see_some_text(page_text, browser):
    page_text = userify(page_text)
    assert browser.is_text_present(page_text), u'Text {} not present on the page {}'.format(
        page_text,
        browser.url
    )


@then(parsers.parse("I click '{button_name}'"))
@then(parsers.parse('I click "{button_name}"'))
def click_some_button(button_name, browser):
    button_name = userify(button_name)
    button = browser.find_by_xpath(
        "//*[contains(text(), '{}')]".format(button_name)
    ).first
    button.click()


@then(parsers.parse("I fill the '{field}' field by '{value}' value"))
@then(parsers.parse('I fill the "{field}" field by "{value}" value'))
def fill_field_with_text(field, value, browser):
    value = userify(value)
    browser.fill(field, value)


@then(parsers.parse("I go '{new_url}'"))
@when(parsers.parse("I go '{new_url}'"))
@then(parsers.parse('I go "{new_url}"'))
@when(parsers.parse('I go "{new_url}"'))
def i_go(new_url, browser, web_ui):
    new_url = userify(new_url)
    if new_url.endswith('/'):
        new_url = new_url[:-1]
    browser.visit('{}{}'.format(web_ui['url'], new_url))

# @when('I click the "confirm" button')
# def i_click_the_confirm_button():
#     """I click the "confirm" button."""
#     return


# @when('I enter new value in the SMP update form')
# def i_enter_new_value_in_the_dcp_update_form():
#     """I enter new value in the SMP update form."""
#     return


# @when('click the "update my SMP" button')
# def click_the_update_my_dcp_button():
#     """Click the "update my SMP" button."""
#     return


# @when('then I click the "save" button')
# def then_i_click_the_save_button():
#     """Then I click the "save" button."""
#     return


# @then('I see "update my SMP" button')
# def i_see_update_my_dcp_button():
#     """I see ""update my SMP" button."""
#     return


# @then('I see "SMP updated" message')
# def i_see_dcp_updated_message():
#     """I see "SMP updated" message."""
#     return


# @then('I see "save" button')
# def i_see_save_button():
#     """I see "save" button."""
#     return


# @then('I see the "confirm" button')
# def i_see_the_confirm_button():
#     """I see the "confirm" button."""
#     return


# @then('I see the SMP update form')
# def i_see_the_dcp_update_form():
#     """I see the SMP update form."""
#     return
