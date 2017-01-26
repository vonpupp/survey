# -*- coding: utf-8 -*-
# Copyright 2016 Luis Felipe Mileo - <mileo@kmee.com.br> - KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time

from openerp import api, fields, models

EVALUATIOON_360_LIST = []


def evaluation_360(evaluation_func):
    EVALUATIOON_360_LIST.append(evaluation_func)
    return evaluation_360


class HrEvaluationPlanPhase(models.Model):

    _inherit = 'hr_evaluation.plan.phase'

    action = fields.Selection(
        selection_add=[
            ('360', u'360-degree feedback'),
            ('360-anonymous', u'360-degree anonymous feedback'),
        ]
    )


class HrEvaluationEvaluation(models.Model):

    _inherit = 'hr_evaluation.evaluation'

    @evaluation_360
    def _get_360_evaluation_child(self, evaluation):
        return evaluation.employee_id.child_ids.user_id

    @evaluation_360
    def _get_360_evaluation_parent(self, evaluation):
        return evaluation.employee_id.parent_id.user_id

    @evaluation_360
    def _get_360_evaluation_myself(self, evaluation):
        return evaluation.employee_id.user_id

    @evaluation_360
    def _get_360_evaluation_department(self, evaluation):
        employee_ids = self.env['hr.employee'].search(
            [('department_id', '=',
              evaluation.employee_id.department_id.id)]
        )
        res_users = self.env['res.users']
        for item in employee_ids:
            res_users |= item.user_id
        return res_users

    @api.multi
    def button_plan_in_progress(self):
        """
        TODO: Docstring
        :return:
        """
        super(HrEvaluationEvaluation, self).button_plan_in_progress()
        hr_eval_inter_obj = self.env['hr.evaluation.interview']
        for evaluation in self:
            wait = False
            for phase in evaluation.plan_id.phase_ids:
                if phase.action in ('360', '360-anonymous'):
                    children = self.env['res.users']
                    for item in EVALUATIOON_360_LIST:
                        children |= item(self, evaluation)

                    for child in children:
                        int_id = hr_eval_inter_obj.create({
                            'evaluation_id': evaluation.id,
                            'phase_id': phase.id,
                            'deadline': evaluation.date,
                            'user_id': child.id,
                        })
                        if phase.wait:
                            wait = True
                        if not wait:
                            int_id.survey_req_waiting_answer()

                        if (not wait) and phase.mail_feature:
                            body = phase.mail_body % {
                                'employee_name': child.name,
                                'user_signature': child.user_id.signature,
                                'eval_name': phase.survey_id.title,
                                'date': time.strftime('%Y-%m-%d'),
                                'time': time,
                            }
                            sub = phase.email_subject
                            if child.work_email:
                                vals = {
                                    'state': 'outgoing',
                                    'subject': sub,
                                    'body_html': '<pre>%s</pre>' % body,
                                    'email_to': child.work_email,
                                    'email_from':
                                        evaluation.employee_id.work_email
                                }
                                self.env['mail.mail'].create(vals)
        self.write({'state': 'wait'})


class HrEvaluationInterview(models.Model):

    _inherit = 'hr.evaluation.interview'

    @api.constrains('state')
    def _check_state_done(self):
        for item in self.sudo():
            if (item.state == 'done' and
                    item.phase_id.action == '360-anonymous' and
                    item.create_uid.id != item.user_to_review_id.user_id.id):
                # Anonymize data
                item.write({'user_id': False,
                            'request_id.partner_id': False,
                            'request_id.email': False})

# Se o entrevistador for o entrevistado nao apagar o usuario
# def write(self, vals)
#  if vals.get('state') == 'done':
#      # se retornar relacional
#      vals.get('phase_id') == '360-anonymous'
#
#      item da entrevista:
#    item.etrevistador('res.users') == entrevistado('res.partner'):
