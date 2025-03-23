from webdriver_factory.Browser import ChromeBrowser, MsEdgeBrowser


class BrowserFactory:
    """Factory para crear instancias de navegadores"""

    @staticmethod
    def get_browser(browser_type):
        browsers = {
            "chrome": ChromeBrowser,
            "edge": MsEdgeBrowser
        }
        if browser_type in browsers:
            return browsers[browser_type]().get_driver()
        else:
            print(f"Navegador '{browser_type}' no soportado")
            return ChromeBrowser().get_driver()
