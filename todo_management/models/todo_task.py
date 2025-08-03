from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Todo Task"

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default="new")

    task_name = fields.Char(required=1, default='New Task')
    name = fields.Char(related='task_name')
    description = fields.Text()
    assign_to = fields.Many2many('res.partner')
    due_date = fields.Datetime(default=fields.datetime.now())

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.write({
                'state': 'in_progress'
            })

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    #     _sql_constraints = [
    #         ('unique_name', 'unique("name")', 'The todo.task name already taken')
    #     ]
    #
    #     @api.constrains('bedrooms')
    #     def _non_zero_bedrooms_checker(self):
    #         for rec in self:
    #             if rec.bedrooms == 0:
    #                 raise ValidationError('Please add a valid number of berdooms !')
    #
    #     @api.constrains('living_area')
    #     def _non_zero_living_area_checker(self):
    #         for rec in self:
    #             if rec.living_area == 0:
    #                 raise ValidationError('Please add a valid value for living area !')
    #
    #     @api.constrains('garden_area')
    #     def _non_zero_garden_area_checker(self):
    #         for rec in self:
    #             if rec.garden:
    #                 if rec.garden_area == 0:
    #                     raise ValidationError('Please add a valid value for garden area !')
    #
    #
    # @api.depends('user_ids')
    # def _compute_user_name(self):
    #     for rec in self:
    #         rec.assign_to = rec.user_ids.complete_name
#
#     @api.onchange('expected_price')
#     def _onchange_expected_price(self):
#         for rec in self:
#             print('inside onchange_expected_price')
#         return {'warning':{'title':'Warning!!','message':'You Changed the Expected Price!', 'type':'warning'}
#                 }
#
#
# class TodoTaskLine(models.Model):
#     _name = 'todo.task.line'
#     _description = 'TodoTask Bedrooms'
#     todo.task_id = fields.Many2one('todo.task')
#     area = fields.Float()
#     description =fields.Char()
