from odoo import fields, models, exceptions


class AssignTask(models.TransientModel):
    _name = 'assign.task'
    _description = 'Assign Task'

    assign_to = fields.Many2many('res.partner', string="Assign To", required=True)

    def action_confirm(self):
        # Get the selected todo.task records from context
        active_ids = self.env.context.get('active_ids', [])
        tasks = self.env['todo.task'].browse(active_ids)

        not_allowed = tasks.filtered(lambda t: t.state not in ['new', 'in_progress'])
        if not_allowed:
            raise exceptions.UserError(
                ("You can only change assignment for tasks in 'New' or 'In Progress' state.\n"
                 "These tasks cannot be updated:\n- %s") % "\n- ".join(not_allowed.mapped('task_name'))
            )

        for task in tasks:
            task.assign_to = [(6, 0, self.assign_to.ids)]
