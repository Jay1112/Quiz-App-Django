from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from .models import *
from .forms import *

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

@login_required(login_url="/register/login/")
def home(request):
	quiz_stack = QuizModel.objects.all()
	index = 1 
	context = {
		"quiz_stack":quiz_stack,
		"index":index,
	}
	return render(request,"dashboard/home.html",context)



@login_required(login_url="/register/login/")
def takeQuiz(request,id):
	questions = QuestionModel.objects.filter(quiz_id=id)
	quiz = QuizModel.objects.get(id=id)

	if request.method == "POST":
		count = QuestionModel.objects.filter(quiz_id=id).count()
		get_answers = []
		counter = 0
		percentage = 0
		for data in range(1,count+1):
			ansSubmit = str(request.POST.get(str(data)))
			ansReal = QuestionModel.objects.filter(id=data)
			ansReal = str(ansReal.values("answer")[0]["answer"])
			get_answers.append([ansSubmit,ansReal])

			if ansSubmit == ansReal:
				counter = counter + 1

		if count != 0:
			percentage = int((counter/count)*100)
		else:
			percentage = 0

		if percentage >= 75:
			display = "" + str(percentage) + "%"
			message = "Congratulations!"
			eligible = True

			context = {
				"display":display,
				"message":message,
				"percentage":percentage,
				"eligible":eligible,
				"get_answers":get_answers,
			}
			return render(request,"dashboard/scoreboard.html",context)
		else:
			display = "" + str(percentage) + "%"
			message = "Sorry!"
			eligible = False
			context = {
				"display":display,
				"message":message,
				"percentage":percentage,
				"eligible":eligible,
				"get_answers":get_answers,
			}
			return render(request,"dashboard/scoreboard.html",context)


	context = {
		"questions":questions,
	}
	return render(request,"dashboard/quiz_page.html",context)

@login_required(login_url="/register/login/")
def results(request):
	return render(request,"dashboard/scoreboard.html",{})

def show(request):
	context = {
		"username":"username",
	}
	return render(request,"dashboard/certificate.html",context)

class ViewPDF(View):
	def get(self, request, *args, **kwargs):
		context = {
			"username" : request.user.username,
		}
		pdf = render_to_pdf('dashboard/certificate.html',context)
		return HttpResponse(pdf, content_type='application/pdf')

class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		context = {
			"username" : request.user.username,
		}
		pdf = render_to_pdf('dashboard/certificate.html', context)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "certificate.pdf"
		content = "attachment; filename=" + filename 
		response['Content-Disposition'] = content
		return response


