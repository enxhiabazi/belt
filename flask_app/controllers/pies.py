from flask_app import app
from flask_app.models.user import User
from flask_app.models.pie import Pie

from flask import render_template, redirect, session, request, flash
#CREATE PIE
@app.route('/create/pie', methods = ['POST'])
def createCar():
    if 'user_id' in session:
        if not Pie.validate_pie(request.form):
            return redirect(request.referrer)
        data = {
            'name': request.form['name'],
            'filling': request.form['filling'],
            'crust': request.form['crust'],
            'user_id': session['user_id']
        }
        Pie.save(data)
        return redirect('/dashboard')
    return redirect('/')

#EDIT PIE
@app.route('/edit/pie/<int:id>')
def editPie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        user = User.get_user_by_id(data)
        pie = Pie.get_pie_by_id(data)
        if user['id'] == pie['user_id']:
            return render_template('editPie.html', user = user, pie = pie)
        return redirect('/dashboard')
    return redirect('/')

#UPDATE PIE
@app.route('/update/pie/<int:id>', methods = ['POST'])
def updatePie(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        user = User.get_user_by_id(data1)
        pie = Pie.get_pie_by_id(data1)
        if user['id'] == pie['user_id']:
            if not Pie.validate_pie(request.form):
                return redirect(request.referrer)
            data = {
            'name': request.form['name'],
            'filling': request.form['filling'],
            'crust': request.form['crust'],
            'pie_id': id
            }
            Pie.update(data)
            return redirect('/')
        return redirect('/dashboard')
    return redirect('/')

#DELETE CAR
@app.route('/delete/pie/<int:id>')
def deletePie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        user = User.get_user_by_id(data)
        pie = Pie.get_pie_by_id(data)
        if user['id'] == pie['user_id']:
            Pie.deleteAllPies(data)
            Pie.delete(data)
            return redirect(request.referrer)
        return redirect('/dashboard')
    return redirect('/')

#SHOW PIE
@app.route('/show/<int:id>')
def showPie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        user = User.get_user_by_id(data)
        pie = Pie.get_pie_by_id(data)
        votes = Pie.get_user_likes_id(data)
        return render_template('showOne.html', user = user, pie= pie, votes= votes)
    return redirect('/')

#Show all pies
@app.route('/showAll')
def showAllPies():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
        }
        user = User.get_user_by_id(data)
        pies = Pie.get_all()
        return render_template('showAllPies.html', pies= pies, user=user)
    return redirect('/')

@app.route('/vote/<int:id>')
def votePie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        voted = User.get_liked_pies(data)
        if id not in voted:
            Pie.addVote(data)
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/unvote/<int:id>')
def unvotePie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        Pie.unVote(data)
        return redirect(request.referrer)
    return redirect('/')
