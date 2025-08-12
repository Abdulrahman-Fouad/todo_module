import json
import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request


def valid_response(data, status, pagination_info={}):
    response_body = {"data": data}
    if pagination_info:
        response_body['pagination_info'] = pagination_info

    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {"error": error}
    return request.make_json_response(response_body, status=status)


class TodoTaskApi(http.Controller):
    @http.route("/v1/todo_task", methods=["POST"], type="http", auth="none", csrf=False)
    def post_task(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        if not vals.get("task_name"):
            return invalid_response("Field name is required", 400)
        try:
            res = request.env['todo.task'].sudo().create(vals)
            if res:
                return valid_response({
                    "message": f"{res.name} has been created successfully",
                    "id": res.id,
                    "name": res.name,
                }, 201)

        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/todo_task/<int:id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_task(self, id):
        try:
            task_id = request.env['todo.task'].sudo().search([('id', '=', id)])
            if not task_id:
                return invalid_response(f"There is no task with id: {id} !!!", 400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            task_id.write(vals)
            return valid_response({
                "message": f"{task_id.name} has been updated successfully",
                "id": task_id.id,
                "name": task_id.name,
            }, 200)
        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/todo_task/<int:id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_task(self, id):
        try:
            task_id = request.env['todo.task'].sudo().search([('id', '=', id)])
            if not task_id:
                return invalid_response(f"There is no task with id: {id} !!!", 400)
            names = task_id.assign_to.mapped('name')
            return valid_response({
                "task_name": task_id.name,
                "description": task_id.description,
                "due_date": task_id.due_date,
                "estimated_time": task_id.estimated_time,
                "state": task_id.state,
                "assign_to": names,
            }, 200)

        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/todo_task/<int:id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_task(self, id):
        try:
            task_id = request.env['todo.task'].sudo().search([('id', '=', id)])
            if not task_id:
                return invalid_response(f"There is no task with id: {id} !!!", 400)
            task_id.unlink()
            return valid_response({
                "messege": f"Task with id: {id} has been deleted successfully",
            }, 200)
        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/todo_tasks", methods=["GET"], type="http", auth="none", csrf=False)
    def get_task_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            task_domain = []
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])

            if page:
                offset = (page * limit) - limit

            if params.get('state'):
                task_domain += [('state', '=', params.get('state')[0])]

            task_ids = request.env['todo.task'].sudo().search(task_domain, offset=offset, limit=limit, order='id desc')
            task_count = request.env['todo.task'].sudo().search_count(task_domain)

            if not task_ids:
                return invalid_response("There are no records !!!", 400)
            return valid_response([{
                "id": task_id.id,
                "task_name": task_id.name,
                "description": task_id.description,
                "due_date": task_id.due_date,
                "estimated_time": task_id.estimated_time,
                "state": task_id.state,
                "assign_to": task_id.assign_to.mapped('name'),
            } for task_id in task_ids],
                pagination_info={'page': page if page else 1,
                                 'limit': limit,
                                 'pages': math.ceil(task_count / limit) if limit else 1,
                                 'count': task_count
                                 },
                status=200)
        except Exception as error:
            return invalid_response(error, 400)
