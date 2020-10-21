from . import main_bp
from app.models import Host
from app.models import db
from flask import jsonify, request
import time
import json


@main_bp.route('/hosts', methods=['GET'])
def get_hosts():
    current_page = request.args.get('current_page', 1, type=int)
    page_size = request.args.get('page_size', type=int)
    print(page_size)
    paginate = Host.query.order_by(Host.create_time.desc()).paginate(
        page=current_page, per_page=page_size, error_out=False)
    hosts = paginate.items
    pages = paginate.pages
    next = None
    if paginate.has_next:
        next = current_page + 1
    prev = None
    if paginate.has_prev:
        prev = current_page - 1

    return jsonify({
        'data': {
            'hosts': [host.to_json() for host in hosts],
            'total': int(paginate.total),
            'next': next,
            'prev': prev,
            'pages': pages
        },
        'msg': "success!",
        'code': 200,
        'extra': {}
    })


@main_bp.route('/host/<int:id>')
def get_host(id):
    host = Host.query.get(id)
    if not host:
        return jsonify({
                        'data': {
                            'host': None,
                        },
                        'msg': "fail!",
                        'code': 404,
                        'extra': {}
                    })
    return jsonify({
                        'data': {
                            'host': host.to_json(),
                        },
                        'msg': "success!",
                        'code': 200,
                        'extra': {}
                    })


@main_bp.route('/add_host', methods=['POST'])
def add_host():
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    name = json_data['name']
    ssh_user = json_data['ssh_user']  
    ssh_password = json_data['ssh_password']  
    in_ipaddr = json_data['in_ipaddr']  
    out_ipaddr = json_data['out_ipaddr']  
    use = json_data['use']  
    is_active = json_data['is_active']
    location =  json_data['location']
    check1 = Host.query.filter_by(in_ipaddr=in_ipaddr).first()
    check2 = Host.query.filter_by(out_ipaddr=out_ipaddr).first()
    if  check1 is not None or check2 is not None:
        return jsonify({
                        'data': {
                        },
                        'msg': "fail!",
                        'code': 500,
                        'extra': {}
                    })
    host = Host(
                    name=name,
                    ssh_user=ssh_user,
                    ssh_password=ssh_password,
                    in_ipaddr=in_ipaddr,
                    out_ipaddr=out_ipaddr,
                    use=use,
                    location=location,
                    is_active=is_active
                    )
    db.session.add(host)
    db.session.commit()
    return jsonify({
                        'data': {
                        },
                        'msg': "success!",
                        'code': 200,
                        'extra': {}
                    })
