from kaylee.testsuite import KayleeTest, load_tests
from kaylee.project import Project, AUTO_PROJECT_MODE, MANUAL_PROJECT_MODE
from kaylee.testsuite.helper import NonAbstractProject

class ProjectTests(KayleeTest):
    def setUp(self):
        pass

    def test_project_mode(self):
        # test if initializing Project without a mode raises a ValueError
        class MyProjectNoMode(NonAbstractProject):
            def __init__(self):
                super(MyProjectNoMode, self).__init__("/script.js")

        self.assertRaises(ValueError, MyProjectNoMode)

        # -- test with invalid mode
        class MyProjectInvalidMode(NonAbstractProject):
            mode = 'abc'
            def __init__(self):
                super(MyProjectInvalidMode, self).__init__("/script.js")
        self.assertRaises(ValueError, MyProjectInvalidMode)

        # -- test with valid modes
        class MyProjectWithAutoMode(NonAbstractProject):
            mode = AUTO_PROJECT_MODE
            def __init__(self):
                super(MyProjectWithAutoMode, self).__init__("/script.js")
                Project.__init__(self, "/script.js")
        MyProjectWithAutoMode()

        class MyProjectWithManualMode(NonAbstractProject):
            mode = MANUAL_PROJECT_MODE
            def __init__(self):
                super(MyProjectWithManualMode, self).__init__("/script.js")
        MyProjectWithManualMode()



kaylee_suite = load_tests([ProjectTests, ])
