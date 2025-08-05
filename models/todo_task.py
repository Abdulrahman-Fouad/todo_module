from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Todo Task"

    # ---------------------------------------- Fields Declaration ---------------------------------
    task_name = fields.Char(required=True, default='New Task')
    name = fields.Char(related='task_name')
    description = fields.Text()
    due_date = fields.Datetime(default=fields.datetime.now())
    estimated_time = fields.Float("Estimated Time (hrs)")
    active = fields.Boolean(default=True)
    is_late = fields.Boolean(tracking=True)

    # ---------------------------------------- Special ---------------------------------
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed')
    ], default="new")

    # ---------------------------------------- Relational ---------------------------------
    assign_to = fields.Many2many('res.partner')
    line_ids = fields.One2many('todo.task.line', 'task_id')

    # ---------------------------------------- Action Methods -------------------------------------
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

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    def task_due_date_alarm(self):
        new_and_in_progress_task_ids = self.search([("state","in",['new','in_progress'])])
        for rec in new_and_in_progress_task_ids:
            if rec.due_date and rec.due_date < fields.datetime.now():
                rec.is_late = True

            if rec.due_date and rec.due_date > fields.datetime.now():
                rec.is_late = False

    # ---------------------------------------- Constrains -------------------------------------
    @api.constrains("line_ids")
    def _check_step_time(self):
        for rec in self:
            print(rec.line_ids.mapped("time"))
            total_time = sum(rec.line_ids.mapped("time"))
            if rec.estimated_time and rec.estimated_time < total_time:
                raise exceptions.ValidationError(
                    f"The Total Time {total_time} is greater than the Estimated Time {rec.estimated_time}")


class TodoTaskLines(models.Model):
    _name = 'todo.task.line'
    _description = 'Todo Task Line'

    date = fields.Date()
    description = fields.Text()
    time = fields.Float()
    task_id = fields.Many2one('todo.task')
