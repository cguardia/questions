from .settings import BOOTSTRAP_URL
from .settings import SUGGESTED_JS_BY_PLATFORM
from .settings import SURVEY_JS_CDN


SURVEY_JS = """
Survey
    .StylesManager
    .applyTheme('{}');

var json = {};

var sendDataToServer = function(result) {{

fetch('{}', {{
    method: 'post',
    headers: {{
        'Accept': 'text/html, text/plain, */*',
        'Content-Type': 'application/json'
    }},
    body: JSON.stringify(result.data)
}})
.then(function (response) {{
    return response;
}})
.then(function (result) {{
    console.log('Redirect successful');
}})
.catch (function (error) {{
    console.log('Request failed', error);
}});

}}

{}
"""

PLATFORM_JS= {
    "jquery": """var survey = new Survey.Model(json);
$("#questions_form").Survey({
    model:survey,
    onComplete:sendDataToServer
});
""",
    "angular": """window.survey = new Survey.Model(json);
survey
    .onComplete
    .add(sendDataToServer);
function onAngularComponentInit() {
    Survey
        .SurveyNG
        .render("surveyElement", {model: survey});
}
var QuestionsApp = ng
    .core
    .Component({selector: 'ng-app', template: '<div id="surveyContainer" class="survey-container contentcontainer codecontainer"><div id="surveyElement"></div></div> '})
    .Class({
        constructor: function () {},
        ngOnInit: function () {
            onAngularComponentInit();
        }
    });
document.addEventListener('DOMContentLoaded', function () {
    ng
        .platformBrowserDynamic
        .bootstrap(QuestionsApp);
});
""",
    "ko": """var survey = new Survey.Model(json, "questions_form");
survey.onComplete.add(sendDataToServer);
""",
    "react": """window.survey = new Survey.Model(json);
    ReactDOM.render(<Survey.Survey json={json} onComplete={sendDataToServer}/>,
  document.getElementById("questions_form"));
""",
    "vue": """var survey = new Survey.Model(json);
survey
    .onComplete
    .add(sendDataToServer);
new Vue({ el: '#questions_form', data: { survey: survey } });
""",
}

SURVEY_HTML = {
    "jquery": """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{}</title>
        <meta name="viewport" content="width=device-width"/>
        {}
    </head>
    <body>

        <div id="questions_form" style="display:inline-block;width:100%;"></div>

        <script type="text/javascript">{}</script>

    </body>
</html>
""",
    "angular": """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{}</title>
        <meta name="viewport" content="width=device-width"/>
        {}
    </head>
    <body>

        <ng-app><ng-app>

        <script type="text/javascript">{}</script>

    </body>
</html>
""",
    "ko": """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{}</title>
        <meta name="viewport" content="width=device-width"/>
        {}
    </head>
    <body>

        <div id="questions_form" style="display:inline-block;width:100%;"></div>

        <script type="text/javascript">{}</script>

    </body>
</html>
""",
    "react": """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{}</title>
        <meta name="viewport" content="width=device-width"/>
        {}
    </head>
    <body>

        <div id="questions_form" style="display:inline-block;width:100%;"></div>

        <script type="text/babel">{}</script>

    </body>
</html>
""",
    "vue": """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{}</title>
        <meta name="viewport" content="width=device-width"/>
        {}
    </head>
    <body>

        <div id="questions_form" style="display:inline-block;width:100%;">
            <survey :survey='survey' />
        </div>

        <script type="text/javascript">{}</script>

    </body>
</html>
""",
}


def get_platform_js_resources(platform, resource_url):
    survey_js = f"{resource_url}/survey.{platform}.min.js"
    platform_js = []
    if resource_url == SURVEY_JS_CDN:
        for js in SUGGESTED_JS_BY_PLATFORM[platform]:
            platform_js.append(js)
    platform_js.append(survey_js)
    return platform_js

def get_theme_css_resources(theme, resource_url):
    if theme == "bootstrap" and resource_url == SURVEY_JS_CDN:
        return [BOOTSTRAP_URL]
    elif theme == "bootstrap":
        return [f"{resource_url}/bootstrap.min.css"]
    name = "survey"
    if theme == "modern":
        name = "modern"
    return [f"{resource_url}/{name}.css"]

def get_survey_js(json, action, theme, platform):
    platform_js = PLATFORM_JS[platform]
    return SURVEY_JS.format(theme, json, action, platform_js)

def get_form_page(title, platform, js, js_resources, css_resources):
    resources = ""
    platform_html = SURVEY_HTML[platform]
    for resource in js_resources:
        resources += f'<script src="{resource}"></script>\n'
    for resource in css_resources:
        resources += f'<link href="{resource}" type="text/css" rel="stylesheet" />\n'
    return platform_html.format(title, resources, js)
