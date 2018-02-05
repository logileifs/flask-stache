# -*- coding: utf-8 -*-
"""
    flask_stache
    ~~~~~~~~~~~~

    Simple mustache templating for Flask applications

    :copyright: (c) 2012 by Matt Wright.
    :license: MIT, see LICENSE for more details.
"""

import os

from flask import request, current_app as app

from pystache.renderer import Renderer


def _get_renderer(append=None):
    append = append or []

    dirs = [os.path.join(app.root_path, app.template_folder, *append)]

    bp = app.blueprints.get(request.blueprint, None)
    if bp and bp.template_folder:
        dirs.append(os.path.join(bp.root_path, bp.template_folder, *append))

    return Renderer(search_dirs=dirs)


def render_view(view):
    """Render a view object

    :param view: The view object to render
    """
    return _get_renderer().render(view)


def render_template(template, **context):
    """Renders a given template and context.

    :param template: The template name
    :param context: the variables that should be available in the
                    context of the template.
    """
    parts = template.split('/')
    renderer = _get_renderer(parts[:-1])
    return renderer.render(renderer.load_template(parts[-1:][0]), context)
