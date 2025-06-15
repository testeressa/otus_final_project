import allure


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.logger = browser.logger
        self.class_name = type(self).__name__

    @allure.step
    def open(self, url):
        self.logger.info("%s: Opening url: %s" % (self.class_name, url))
        self.browser.get(url)
