#
# Copyright 2014, Martin Owens <doctormo@gmail.com>
#
# This file is part of the software inkscape-web, consisting of custom 
# code for the Inkscape project's django-based website.
#
# inkscape-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inkscape-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with inkscape-web.  If not, see <http://www.gnu.org/licenses/>.
#

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.admin import *
from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import *

class CarouselPlugin(CMSPluginBase):
    model = Carousel
    name = "Carousel"
    render_template = "cms/plugins/carousel.html"
    allow_children = True
    child_classes = ["CarouselItemPlugin"]

class CarouselItemPlugin(CMSPluginBase):
    model = CarouselItem
    name = "Carousel Item"
    render_template = "cms/plugins/carousel_item.html"
    require_parent = True

plugin_pool.register_plugin(CarouselPlugin)
plugin_pool.register_plugin(CarouselItemPlugin)


class PannelRowPlugin(CMSPluginBase):
    model = PannelRow
    name = "Pannel Row"
    render_template = "cms/plugins/pannel_row.html"
    allow_children = True
    child_classes = ["PannelPlugin"]

class PannelPlugin(CMSPluginBase):
    model = Pannel
    name = "Pannel"
    render_template = "cms/plugins/pannel_item.html"
    require_parent = True

    class Media:
        css = {'all': ('css/icon_list.css',)}

plugin_pool.register_plugin(PannelRowPlugin)
plugin_pool.register_plugin(PannelPlugin)


class PortfolioPlugin(CMSPluginBase):
    model = PortfolioSection
    name = "Portfolio"
    render_template = "cms/plugins/portfolio.html"
    allow_children = True
    child_classes = ["PortfolioItemPlugin"]

class PortfolioItemPlugin(CMSPluginBase):
    model = PortfolioItem
    name = "Pannel"
    render_template = "cms/plugins/portfolio_item.html"
    require_parent = True

plugin_pool.register_plugin(PortfolioPlugin)
plugin_pool.register_plugin(PortfolioItemPlugin)


class CallToActionPlugin(CMSPluginBase):
    model = CallToAction
    name = "Call to Action"
    render_template = "cms/plugins/call_action.html"
    allow_children = True
    child_classes = ["TextPlugin"]

plugin_pool.register_plugin(CallToActionPlugin)

class HrPlugin(CMSPluginBase):
    model = HorizontalRule
    name = "Horizontal Rule"
    render_template = "cms/plugins/hr.html"

plugin_pool.register_plugin(HrPlugin)

class EmbededSvgPlugin(CMSPluginBase):
    model = EmbededSvg
    name = "Embeded SVG Image"
    render_template = "cms/plugins/svg.html"

    def render(self, context, instance, placeholder):
        context['svg'] = instance.svg_file.read()
        return context

plugin_pool.register_plugin(EmbededSvgPlugin)

