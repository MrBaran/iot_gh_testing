from integration_tests import IntegrationTests

def main():
    test_service = IntegrationTests()
    test_service.test_all()

if __name__ == "__main__":
    main()


