# coding=utf-8
from celery_tasks.main import app
from libs.yuntongxun.sms import CCP


@app.task(name='发送短信')
def send_sms_code(mobile, sms_code):
    """发送短信任务"""
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, 5], 1)