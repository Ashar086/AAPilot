from flask import render_template
from . import bp

@bp.route('/received/aa-card')
def received_aa_card():
    return render_template('recipient/received.shared.aa-card.html')

@bp.route('/received/link')
def received_link():
    return render_template('recipient/received.shared.link.html')

@bp.route('/match-sample')
def match_sample():
    return render_template('recipient/matchSample.html')

@bp.route('/assessment-start')
def assessment_start():
    return render_template('shared/assessment-start.html')

@bp.route('/register')
def register():
    return render_template('shared/register.html')

@bp.route('/results')
def results():
    return render_template('shared/results.html')

@bp.route('/matchability-compare')
def matchability_compare():
    return render_template('shared/result.matchabilityCompare.html')

@bp.route('/share')
def share():
    return render_template('shared/share.html')
