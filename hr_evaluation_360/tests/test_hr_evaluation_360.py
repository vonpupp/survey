# -*- coding: utf-8 -*-

from openerp.tests import common


class TestHrEvaluation360(common.TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestHrEvaluation360, self).setUp(*args, **kwargs)
        cr, uid = self.cr, self.uid

        # Usefull models
        self.hr_employee = self.registry('hr.employee')
        # self.hr_holidays = self.registry('hr.holidays')
        # self.hr_holidays_status = self.registry('hr.holidays.status')
        self.res_users = self.registry('res.users')
        self.res_partner = self.registry('res.partner')

        # Find Employee group
        group_employee_ref = self.registry('ir.model.data').get_object_reference(cr, uid, 'base', 'group_user')
        self.group_employee_id = group_employee_ref and group_employee_ref[1] or False

        # Find Hr User group
        group_hr_user_ref = self.registry('ir.model.data').get_object_reference(cr, uid, 'base', 'group_hr_user')
        self.group_hr_user_ref_id = group_hr_user_ref and group_hr_user_ref[1] or False

        # Find Hr Manager group
        group_hr_manager_ref = self.registry('ir.model.data').get_object_reference(cr, uid, 'base', 'group_hr_manager')
        self.group_hr_manager_ref_id = group_hr_manager_ref and group_hr_manager_ref[1] or False

        # Test partners to use through the various tests
        self.hr_partner_id = self.res_partner.create(cr, uid, {
            'name': 'Gertrude AgrolaitPartner',
            'email': 'gertrude.partner@agrolait.com',
        })
        self.email_partner_id = self.res_partner.create(cr, uid, {
            'name': 'Patrick Ratatouille',
            'email': 'patrick.ratatouille@agrolait.com',
        })

        # Test users to use through the various tests
        self.user_hruser_id = self.res_users.create(cr, uid, {
            'name': 'Armande HrUser',
            'login': 'Armande',
            'alias_name': 'armande',
            'email': 'armande.hruser@example.com',
            'groups_id': [(6, 0, [self.group_employee_id, self.group_hr_user_ref_id])]
        }, {'no_reset_password': True})
        self.user_hrmanager_id = self.res_users.create(cr, uid, {
            'name': 'Bastien HrManager',
            'login': 'bastien',
            'alias_name': 'bastien',
            'email': 'bastien.hrmanager@example.com',
            'groups_id': [(6, 0, [self.group_employee_id, self.group_hr_manager_ref_id])]
        }, {'no_reset_password': True})
        self.user_none_id = self.res_users.create(cr, uid, {
            'name': 'Charlie Avotbonkeur',
            'login': 'charlie',
            'alias_name': 'charlie',
            'email': 'charlie.noone@example.com',
            'groups_id': [(6, 0, [])]
        }, {'no_reset_password': True})
        self.user_employee_id = self.res_users.create(cr, uid, {
            'name': 'David Employee',
            'login': 'david',
            'alias_name': 'david',
            'email': 'david.employee@example.com',
            'groups_id': [(6, 0, [self.group_employee_id])]
        }, {'no_reset_password': True})

        # Hr Data
        self.employee_emp_id = self.hr_employee.create(cr, uid, {
            'name': 'David Employee',
            'user_id': self.user_employee_id,
        })
        self.employee_hruser_id = self.hr_employee.create(cr, uid, {
            'name': 'Armande HrUser',
            'user_id': self.user_hruser_id,
        })

    def test_01_anonymous_employee_self_appraisal_keeps_name(self):
        """
        On an anonymous 360 survey when an employee creates a self appraisal,
        the name of the appraiser should be keeped
        """
        # user_vonpupp = self.env.ref('base.user_vonpupp')
        # self.env = self.env(user=user_demo)
        Survey = self.env['survey.survey']
        Plan = self.env['hr_evaluation.plan']
        Phase = self.env['hr_evaluation.plan.phase']
        Evaluation = self.env['hr_evaluation.evaluation']

        survey = Survey.create({
            'title': 'survey title'
        })

        plan_360_anonymous = Plan.create({
            'name': 'plan',
            'company_id': '1',
            'month_first': 3,
            'month_next': 6,
            'active': True,
        })
        import ipdb; ipdb.set_trace() # BREAKPOINT
        #plan = Plan.search('name', 'ilike', '%Manager%')

        send_phase = Phase.create({
            'name': 'test_appraisal_plan',
            'sequence': '1',
            'company_id': '1',
            'plan_id': plan_360_anonymous.id,
            'action': '360-anonymous',
            'survey_id': survey.id,
            # 'survey_id': fields.many2one('survey.survey', 'Appraisal Form', required=True),
            # 'send_answer_manager': fields.boolean('All Answers',
            #     help="Send all answers to the manager"),
            # 'send_answer_employee': fields.boolean('All Answers',
            #     help="Send all answers to the employee"),
            # 'send_anonymous_manager': fields.boolean('Anonymous Summary',
            #     help="Send an anonymous summary to the manager"),
            # 'send_anonymous_employee': fields.boolean('Anonymous Summary',
            #     help="Send an anonymous summary to the employee"),
            # 'wait': fields.boolean('Wait Previous Phases',
            #     help="Check this box if you want to wait that all preceding phases " +
            #       "are finished before launching this phase."),
            # 'mail_feature': fields.boolean('Send mail for this phase', help="Check this box if you want to send mail to employees coming under this phase"),
            # 'mail_body': fields.text('Email'),
            # 'email_subject': fields.text('Subject')
        })

        evaluation = Evaluation.create({
            'date': '2017-02-20',
            'employee_id': self.employee_emp_id,
            'plan_id': plan_360_anonymous.id,
            #'state': 'done',
        })
        evaluation.button_plan_in_progress()
        import ipdb; ipdb.set_trace() # BREAKPOINT

        #self.assertEqual(task.is_done, False)
        pass

    def test_02_anonymous_employee_appraisal_deletes_name(self):
        pass

    def test_03_anonymous_employee_apraisal_keeps_date(self):
        pass
