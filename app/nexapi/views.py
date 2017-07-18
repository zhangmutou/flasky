import requests, json
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import nexapi
from .. import db
from ..models import NexApiCase
from ..decorators import admin_required, permission_required

@nexapi.route('/show', methods=['GET'])
@login_required
@admin_required
def show_all():
    page = request.args.get('page',1, type=int)
    pagination = NexApiCase.query.paginate(page, per_page=current_app.config['NEX_API_CASES_PER_PAGE'], error_out=True)
    cases = pagination.items
    return render_template('nexapi/nex_api.html', cases=cases, pagination=pagination)


@nexapi.route('/get')
@login_required
@admin_required
def get_case():
    id = request.args.get('id')
    case = NexApiCase.query.filter_by(id=id).first()
    # c = []
    d = {}
    for column in case.__table__.columns:
        d[column.name] = str(getattr(case, column.name))
    # c.append(d)
    return jsonify({'msg':d})


@nexapi.route('/update', methods=['POST'])
@login_required
@admin_required
def update_case():
    id = request.values.get('id')
    case = NexApiCase.query.filter_by(id=id).first()
    case.name = request.values.get('name')
    case.desc = request.values.get('desc')
    case.url = request.values.get('curl')
    case.request_type = request.values.get('type')
    case.request_data = request.values.get('data')
    case.expectation = request.values.get('expectation')
    try:
        db.session.commit()
        return jsonify({'msg':'case.url'})
    except Exception as e:
        return jsonify({'msg':e})


@nexapi.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete_case():
    try:
        id = request.values.get('id')
        case = NexApiCase.query.filter_by(id=id).first()
        db.session.delete(case)
        db.session.commit()
        return jsonify({'msg':'删除成功'})
    except Exception as e:
        return jsonify({'msg':e})



@nexapi.route('/exc', methods=['POST'])
@login_required
@admin_required
def exc_case():
    case_ids = request.values.getlist('ids[]')
    total_num = len(case_ids)
    succeed_num = 0
    failed_num = 0
    failed_id = []
    # return jsonify({'msg':case_ids})
    for case_id in case_ids:
        case = NexApiCase.query.filter_by(id=case_id).first()
        expectation = case.expectation
        req_type = case.request_type
        if req_type == 'post':
            s = req_api(case.url, case.request_data)
            # return jsonify({'msg':[json.loads(expectation)]})
            if json.loads(expectation) == s:
                succeed_num += 1
            else:
                failed_num += 1
                failed_id.append(case_id)
    message = {'msg':{'total_num':total_num, 'succeed_num':succeed_num, 'failed_num':failed_num, 'failed_id':failed_id}}
    flash("用例执行成功，详情请在测试报告查看。本次执行报告id: {}".format(1))
    return jsonify(message)


@nexapi.route('/send', methods=['POST'])
@login_required
@admin_required
def send():
    id = request.values.get('id')
    case = NexApiCase.query.filter_by(id=id).first()
    # req_url = 'http://10.165.124.28:8000' + case.url
    # s = requests.post(req_url, data=case.request_data)
    s = req_api(url=case.url, data=case.case_data)
    return jsonify({'msg':{'状态码: ':s.status_code, '地址: ':s.url, '参数: ':case.request_data, '结果: ':s.json()}})


@nexapi.route('/nex-api-auto/test', methods=['POST'])
@login_required
@admin_required
def test():
    ids = request.values.getlist('ids[]')
    return jsonify({'msg':ids})


def req_api(url, case_data):
    req_url = 'http://10.165.124.28:8000' + url
    s = requests.post(req_url, data=case_data).json()
    return s