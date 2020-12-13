from typing import Any
from typing import Dict
from typing import List
from typing import Union
from pydantic import BaseModel
from pydantic import Extra
from pydantic import HttpUrl

try:
    from typing import Literal
except ImportError:  # pragma: NO COVER
    from typing_extensions import Literal

from . import settings
from .utils import get_params_for_repr


class _Base(BaseModel):
    """Base class for questions classes. Main responsibility is renaming
    Python parameter names to Javascript's camelCase convention."""

    def __repr__(self):
        class_name = self.__class__.__name__
        params = get_params_for_repr(dict(self))
        return f"{class_name}({params}\n    )"

    class Config:

        fields = {
            "kind": "type",
            "all_rows_required": "isAllRowRequired",
            "expression_format": "format",
            "max_value": "max",
            "min_value": "min",
            "required": "isRequired",
        }

        @classmethod
        def fix_name(cls, name):
            words = name.split("_")
            name = ""
            for index, word in enumerate(words):
                if index == 0:
                    name += word
                else:
                    name += word.capitalize()
            return name

        extra = Extra.allow
        alias_generator = fix_name


class Validator(_Base):
    """Base class for all validators."""

    kind: str
    message: str = "Invalid value"


class TextValidator(Validator):
    """Validator for text input."""

    kind: str = "text"
    max_length: int = 0
    min_length: int = 0
    allow_digits: bool = True


class NumericValidator(Validator):
    """Validator for numeric input."""

    kind: str = "numeric"
    max_value: int = 0
    min_value: int = 0


class EmailValidator(Validator):
    """Checks if a value is a valid email address."""

    kind: str = "email"


class RegexValidator(Validator):
    """Checks if a value matches a regular expression."""

    kind: str = "regex"
    regex: str = ""


class ExpressionValidator(Validator):
    """Checks if a question's answer matches a set of conditions."""

    kind: str = "regex"
    expression: str = ""


class Question(_Base):
    """
    Base question class. All questions share these properties, and all can be
    set by passing them as parameters when instantiating the question.
    """

    kind: str
    name: str = ""
    title: Union[str, Dict[str, str]] = ""
    description: Union[str, Dict[str, str]] = ""
    required: bool = False
    visible: bool = True
    default_value: str = ""
    correct_answer: str = ""
    visible_if: str = ""
    enable_if: str = ""
    start_with_new_line: bool = True
    value_name: str = ""
    required_if: str = ""
    required_error_text: str = ""
    hide_number: bool = True
    indent: int = 0
    title_location: Literal[settings.TITLE_LOCATIONS] = "default"
    description_location: Literal[settings.DESCRIPTION_LOCATIONS] = "default"
    width: str = ""
    max_width: str = "initial"
    min_width: str = "300px"
    use_display_values_in_title: bool = True
    validators: List[Validator] = []
    extra_js: List[HttpUrl] = []
    extra_css: List[HttpUrl] = []


class TextQuestion(Question):
    """
    A question that uses a text input box. It can handle all HTML5 text input
    types.
    """

    kind: str = "text"
    place_holder: Union[str, Dict[str, str]] = ""
    input_type: Literal[settings.TEXT_INPUT_TYPES] = "text"
    max_length: int = -1
    max_value: str = ""
    min_value: str = ""
    size: int = 0
    step: str = ""
    text_update_mode: Literal[settings.TEXT_UPDATE_MODES] = "default"
    input_mask: str = ""
    input_format: str = ""
    prefix: str = ""
    auto_unmask: bool = True
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://unpkg.com/inputmask@5.0.3/dist/inputmask.js",
    ]


class ChoicesQuestion(Question):
    """
    Base class for questions that let the user select one or more options
    from a list of choices. The choices can either be set at question
    instantiation time, or come from a JSON web service at run time.
    """

    kind: str = ""
    col_count: int = 4
    choices: List[Union[str, Dict[str, Union[str, HttpUrl]]]] = []
    choices_by_url: Dict[Literal[settings.CHOICES_BY_URL_KEYS], str] = []
    choices_order: Literal[settings.CHOICE_ORDER_VALUES] = "none"
    choices_enable_if: str = ""
    choices_visible_if: str = ""
    hide_if_choices_empty: bool = True
    has_other: bool = False
    other_text: Union[str, Dict[str, str]] = "Other"
    other_error_text: Union[str, Dict[str, str]] = ""
    other_place_holder: Union[str, Dict[str, str]] = ""


class RadioGroupQuestion(ChoicesQuestion):
    """
    Select one option from a group of radio buttons.
    """

    kind: str = "radiogroup"
    show_clear_button: bool = False


class DropdownQuestion(ChoicesQuestion):
    """
    Select one option from a dropdown menu.
    """

    kind: str = "dropdown"
    choices_max: int = 0
    choices_min: int = 0
    choices_step: int = 1
    options_caption: str = ""
    show_options_caption: bool = True


class CheckboxQuestion(ChoicesQuestion):
    """
    Select one or more options from a group of check boxes.
    """

    kind: str = "checkbox"
    has_none: bool = False
    has_select_all: bool = False
    none_text: Union[str, Dict[str, str]] = "None"
    select_all_text: Union[str, Dict[str, str]] = ""


class ImagePickerQuestion(ChoicesQuestion):
    """
    Display a group of images and let the user pick one or more.
    """

    kind: str = "imagepicker"
    content_mode: Literal[settings.IMAGE_CONTENT_MODE_VALUES] = "image"
    show_label: bool = False
    image_height: int = 200
    image_width: int = 300
    image_fit: Literal[settings.IMAGE_FIT_VALUES] = "none"
    multi_select: bool = False
    has_other: bool = False
    other_text: Union[str, Dict[str, str]] = "Other"
    other_error_text: Union[str, Dict[str, str]] = ""
    other_place_holder: Union[str, Dict[str, str]] = ""


class BooleanQuestion(Question):
    """
    Get the answer for any two-possibility question. Usually true/false, yes/
    no questions.
    """

    kind: str = "boolean"
    label_true: Union[str, Dict[str, str]] = ""
    label_false: Union[str, Dict[str, str]] = ""
    show_title: bool = False
    value_true: Union[str, Dict[str, str]] = "true"
    value_false: Union[str, Dict[str, str]] = "false"


class SignaturePadQuestion(Question):
    """
    Allow the user to "sign" something by drawing their signature. Can be used
    to capture user drawings for other types of questions.
    """

    kind: str = "signaturepad"
    height: int = 200
    width: int = 300
    allow_clear: bool = True


class MultipleTextQuestion(Question):
    """
    A text question with multiple related parts. Displays a text box for each
    part.
    """

    kind: str = "multipletext"
    col_count: int = 2
    items: List[Dict[str, str]] = []
    item_size: int = 0


class CommentQuestion(Question):
    """
    A question that uses a text area to get a multi-line text answer.
    """

    kind: str = "comment"
    rows: int = 3
    cols: int = 50
    max_length: int = -1
    place_holder: Union[str, Dict[str, str]] = ""
    text_update_mode: Literal[settings.TEXT_UPDATE_MODES] = "default"


class RatingQuestion(Question):
    """
    A question that lets the user select a number on a fixed scale.
    """

    kind: str = "rating"
    min_rate_description: Union[str, Dict[str, str]] = ""
    max_rate_description: Union[str, Dict[str, str]] = ""
    rate_max: int = 5
    rate_min: int = 1
    rate_step: int = 1
    rate_values: List[Union[int, Dict[str, Union[int, str]]]] = []


class FileQuestion(Question):
    """
    A question for uploading one or more files.
    """

    kind: str = "file"
    show_preview: bool = True
    allow_multiple: bool = False
    store_data_as_text: bool = True
    image_height: int = 100
    image_width: int = 150
    max_size: int = 0
    accepted_types: str = ""
    allow_images_preview: bool = True
    need_confirm_remove_file: bool = False
    wait_for_upload: bool = True


class MatrixQuestion(Question):
    """
    A question that displays rows of radio buttons and allows the user to
    select a value from one of several columns for each row.
    """

    kind: str = "matrix"
    columns: List[Any]
    rows: List[Any] = []
    all_rows_required: bool = False
    cells: Dict[str, Dict[str, str]] = {}
    columns_visible_if: str = ""
    rows_order: Literal[settings.ROW_ORDER_VALUES] = "initial"
    rows_visible_if: str = ""
    show_header: bool = True


class MatrixDropdownQuestion(Question):
    """
    A matrix question that can include other types of input controls, like
    dropdowns and text boxes.
    """

    kind: str = "matrixdropdown"
    columns: List[Any]
    rows: List[Any] = []
    all_rows_required: bool = False
    cells: Dict[str, Dict[str, Any]] = {}
    columns_visible_if: str = ""
    rows_order: Literal[settings.ROW_ORDER_VALUES] = "initial"
    rows_visible_if: str = ""
    show_header: bool = True
    cell_type: Literal[settings.MATRIX_CELL_TYPES] = "dropdown"
    choices: List[Any] = []
    column_col_count: int = 1
    column_layout: Literal[settings.MATRIX_COLUMN_LAYOUTS] = "horizontal"
    column_min_width: str = ""
    horizontal_scroll: bool = False
    options_caption: str = ""
    row_title_width: str = ""
    total_text: str = ""


class MatrixDynamicQuestion(Question):
    """
    A matrix dropdown question that allows the user to add or remove new rows
    from their answer.
    """

    kind: str = "matrixdynamic"
    columns: List[Any]
    rows: List[Any] = []
    all_rows_required: bool = False
    cells: Dict[str, Dict[str, Any]] = {}
    columns_visible_if: str = ""
    rows_order: Literal[settings.ROW_ORDER_VALUES] = "initial"
    rows_visible_if: str = ""
    show_header: bool = True
    cell_type: Literal[settings.MATRIX_CELL_TYPES] = "dropdown"
    choices: List[Any] = []
    column_col_count: int = 1
    column_layout: Literal[settings.MATRIX_COLUMN_LAYOUTS] = "horizontal"
    column_min_width: str = ""
    horizontal_scroll: bool = False
    options_caption: str = ""
    add_row_location: Literal[settings.MATRIX_ROW_LOCATIONS] = "default"
    add_row_text: str = ""
    allow_add_rows: bool = True
    allow_remove_rows: bool = True
    confirm_delete: bool = False
    confirm_delete_text: str = ""
    default_row_value: Any = ""
    default_value_from_last_row: bool = False
    key_duplication_error: str = ""
    key_name: str = ""
    max_row_count: int = 100
    min_row_count: int = 1
    remove_row_text: str = ""
    row_count: int = 1


class TagBoxQuestion(DropdownQuestion):
    """
    A question that uses the Select2 tag box widget.
    """

    kind: str = "tagbox"
    select2_config: str = ""
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/js/select2.min.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/css/select2.min.css",
    ]


class JQueryUIDatePickerQuestion(TextQuestion):
    """
    A question that uses the JQueryUI date picker.
    """

    kind: str = "datepicker"
    date_format: str = "mm/dd/yy"
    config: str = ""
    max_date: str = ""
    min_date: str = ""
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://code.jquery.com/ui/1.11.4/jquery-ui.min.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.18/themes/smoothness/jquery-ui.css",
    ]


class BootstrapDatePickerQuestion(TextQuestion):
    """
    A question that uses the bootstrap date picker.
    """

    kind: str = "bootstrapdatepicker"
    date_format: str = "mm/dd/yy"
    start_date: str = ""
    end_date: str = ""
    today_highlight: bool = True
    week_start: int = 0
    clear_button: bool = False
    auto_close: bool = True
    days_of_week_highlighted: str = ""
    disable_touch_keyboard: bool = True
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://unpkg.com/moment@2.24.0/moment.js",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css",
    ]


class Select2Question(DropdownQuestion):
    """
    A question that uses the Select2 dropdown widget.
    """

    render_as: str = "select2"
    select2_config: str = ""
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/js/select2.min.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/css/select2.min.css",
    ]


class BarRatingQuestion(DropdownQuestion):
    """
    A question that uses the JQuery bar rating widget.
    """

    kind: str = "barrating"
    rating_theme: Literal[settings.BAR_RATING_THEMES] = "fontawesome-stars"
    show_values: bool = False
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://unpkg.com/jquery-bar-rating",
    ]
    extra_css: List[HttpUrl] = [
        "https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-1to10.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-movie.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-pill.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-reversed.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-horizontal.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/fontawesome-stars.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/css-stars.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/fontawesome-stars-o.css",
    ]


class SortableJSQuestion(CheckboxQuestion):
    """
    A question that uses the JQuery sortable widget.
    """

    kind: str = "sortablelist"
    empty_text: str = ""
    max_answers_count: int = -1
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://unpkg.com/sortablejs@1.7.0/Sortable.js",
    ]


class NoUISliderQuestion(Question):
    """
    A question that uses the NoUISlider JQuery widget.
    """

    kind: str = "nouislider"
    step: int = 1
    range_min: int = 0
    range_max: int = 100
    pips_mode: str = "positions"
    pips_values: List[int] = [0, 25, 50, 75, 100]
    pips_text: List[Union[int, str]] = [0, 25, 50, 75, 100]
    pips_density: int = 5
    orientation: str = "horizontal"
    direction: str = "ltr"
    tooltips: bool = True
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://unpkg.com/nouislider@9.2.0/distribute/nouislider.js",
        "https://unpkg.com/wnumb@1.1.0",
    ]
    extra_css: List[HttpUrl] = [
        "https://unpkg.com/nouislider@9.2.0/distribute/nouislider.min.css",
    ]


class CKEditorQuestion(Question):
    """
    A question that uses the CKEditor JQuery widget.
    """

    kind: str = "editor"
    height: str = "300px"
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://cdn.ckeditor.com/4.14.1/standard/ckeditor.js",
    ]


class BootstrapSliderQuestion(Question):
    """
    A question that uses the bootstrap slider widget.
    """

    kind: str = "bootstrpslider"
    step: int = 1
    range_min: int = 0
    range_max: int = 100
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/10.0.0/bootstrap-slider.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/10.0.0/css/bootstrap-slider.css",
    ]


class EmotionsRatingQuestion(DropdownQuestion):
    """
    A question that uses the emotion ratings JQuery widget.
    """

    kind: str = "emotionsratings"
    emotions: List[str] = ["angry", "disappointed", "meh", "happy", "inLove"]
    emotion_size: int = 30
    emotions_count: int = 5
    bg_emotion: str = "happy"
    emotion_color: str = "FF0066"
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
        "https://unpkg.com/emotion-ratings@2.0.1/dist/emotion-ratings.js",
    ]


class MicrophoneQuestion(Question):
    """
    A question that uses the RecordRTC sound recording widgets.
    """

    kind: str = "microphone"
    extra_js: List[HttpUrl] = [
        "https://www.WebRTC-Experiment.com/RecordRTC.js",
    ]


class HtmlBlock(Question):
    """
    An HTML block that can be embedded in a form.
    """

    kind: str = "html"
    html: Union[str, Dict[str, str]] = ""


class ImageBlock(Question):
    """
    An block for inserting an image in a form.
    """

    kind: str = "image"
    image_height: int = 200
    image_width: int = 300
    image_fit: Literal[settings.IMAGE_FIT_VALUES] = "none"
    image_link: HttpUrl
    content_mode: Literal[settings.IMAGE_CONTENT_MODE_VALUES] = "image"


class ExpressionBlock(Question):
    """
    A block that inserts the result of an expression in a form.
    """

    kind: str = "expression"
    expression: str
    currency: str = "USD"
    display_style: Literal[settings.EXPRESSION_DISPLAY_STYLES] = "none"
    expression_format: str = ""
    maximum_fraction_digits: int = -1
    minimum_fraction_digits: int = -1
    use_grouping: bool = True


class PanelBlock(Question):
    """
    A form panel is a group of questions that go together. A form can contain
    any number of panels, even nested.
    """

    kind: str = "panel"
    inner_indent: int = 1
    elements: List[Question] = []
    question_start_index: str = ""
    question_title_location: Literal[settings.TITLE_LOCATIONS] = "default"
    show_number: bool = False
    show_question_numbers: Literal[settings.SHOW_QUESTION_NUMBERS_VALUES] = "default"
    state: Literal[settings.PANEL_STATES] = "default"


class PanelDynamicBlock(Question):
    """
    Dynamic blocks allow users to manually add or remove panels. A form can contain
    any number of dynamic panels, even nested.
    """

    kind: str = "paneldynamic"
    inner_indent: int = 1
    render_mode: Literal[settings.PANEL_RENDER_MODES] = "list"
    panel_count: int = 1
    panel_add_text: Union[str, Dict[str, str]] = ""
    panel_remove_text: Union[str, Dict[str, str]] = ""
    template_title: Union[str, Dict[str, str]] = ""
    template_elements: List[Question] = []
    allow_add_panel: bool = True
    allow_remove_panel: bool = True
    confirm_delete: bool = False
    confirm_delete_text: Union[str, Dict[str, str]] = ""
    default_value_from_last_panel: bool = False
    key_duplication_error: Union[str, Dict[str, str]] = ""
    key_name: str = ""
    max_panel_count: int = 100
    min_panel_count: int = 1
    panel_add_text: Union[str, Dict[str, str]] = ""
    panel_next_text: Union[str, Dict[str, str]] = ""
    panel_prev_text: Union[str, Dict[str, str]] = ""
    panel_remove_text: Union[str, Dict[str, str]] = ""
    panels_state: Literal[settings.PANEL_STATES] = "default"
    show_question_numbers: Literal[settings.SHOW_QUESTION_NUMBERS_VALUES] = "default"
    show_range_in_progress: bool = True
    template_description: Union[str, Dict[str, str]] = ""
    template_title_location: Literal[settings.TITLE_LOCATIONS] = "default"


class Page(_Base):
    """
    A group of questions presented as an individual form page. A form can contain
    any number of pages.
    """

    name: str = ""
    title: Union[str, Dict[str, str]] = ""
    questions: List[Question] = []
    description: Union[str, Dict[str, str]] = ""
    max_time_to_finish: int = 0
    navigation_buttons_visibility: Literal[settings.NAV_BUTTONS_VISIBILITY] = "inherit"
    question_title_location: Literal[settings.TITLE_LOCATIONS] = "default"
    questions_order: Literal[settings.QUESTION_ORDER_VALUES] = "default"


class Survey(_Base):
    """
    The main SurveyJS form container. Questions forms generate a survey
    rendering the questions contained in a form.
    """

    title: Union[str, Dict[str, str]] = ""
    pages: List[Page] = []
    calculated_values: List[Any] = []
    check_errors_mode: Literal[settings.CHECK_ERRORS_MODES] = "onNextPage"
    clear_invisible_values: Literal[settings.CLEAR_INVISIBLE_VALUES] = "onComplete"
    completed_before_html: Union[str, Dict[str, str]] = ""
    completed_html: Union[str, Dict[str, str]] = ""
    completed_html_on_condition: List[Dict[str, str]] = []
    complete_text: Union[str, Dict[str, str]] = ""
    cookie_name: str = ""
    description: Union[str, Dict[str, str]] = ""
    edit_text: Union[str, Dict[str, str]] = ""
    first_page_is_started: bool = False
    focus_first_question_automatic: bool = True
    focus_on_first_error: bool = True
    go_next_page_automatic: bool = False
    loading_html: Union[str, Dict[str, str]] = ""
    locale: Literal[settings.LOCALES] = ""
    logo: HttpUrl = ""
    logo_fit: Literal[settings.IMAGE_FIT_VALUES] = "contain"
    logo_height: int = 200
    logo_position: Literal[settings.LOGO_POSITIONS] = "left"
    logo_width: int = 300
    max_others_length: int = 0
    max_text_length: int = 0
    max_time_to_finish: int = 0
    mode: Literal[settings.SURVEY_MODES] = "edit"
    navigate_to_url: HttpUrl = ""
    navigate_to_url_on_condition: List[Dict[str, HttpUrl]] = []
    page_next_text: Union[str, Dict[str, str]] = ""
    page_prev_text: Union[str, Dict[str, str]] = ""
    preview_text: Union[str, Dict[str, str]] = ""
    progress_bar_type: Literal[settings.PROGRESS_BAR_TYPES] = "pages"
    question_description_location: Literal[
        settings.QUESTION_DESCRIPTION_LOCATIONS
    ] = "underTitle"
    question_error_location: Literal[settings.QUESTION_ERROR_LOCATIONS] = "top"
    questions_on_page_mode: Literal[settings.QUESTION_PAGE_MODES] = "standard"
    questions_order: Literal[settings.QUESTION_ORDER_VALUES] = "initial"
    question_start_index: str = ""
    question_title_location: Literal[settings.TITLE_LOCATIONS] = "top"
    question_title_pattern: str = "numTitleRequire"
    question_title_template: str = ""
    required_text: Union[str, Dict[str, str]] = "*"
    send_result_on_page_next: bool = False
    show_completed_page: bool = False
    show_navigation_buttons: Literal[settings.NAV_BUTTONS_POSITIONS] = "bottom"
    show_page_numbers: bool = True
    show_page_titles: bool = True
    show_prev_button: bool = True
    show_preview_before_complete: Literal[settings.SHOW_PREVIEW_VALUES] = "noPreview"
    show_progress_bar: Literal[settings.SHOW_PROGRESS_BAR_OPTIONS] = "off"
    show_question_numbers: Literal[settings.PAGE_SHOW_QUESTION_NUMBERS_VALUES] = "on"
    show_timer_panel: Literal[settings.SHOW_TIMER_VALUES] = "none"
    show_timer_panel_mode: Literal[settings.SHOW_TIMER_MODES] = "all"
    show_title: bool = True
    start_survey_text: Union[str, Dict[str, str]] = ""
    store_others_as_comment: bool = True
    survey_id: str = ""
    survey_post_id: str = ""
    survey_show_data_saving: bool = True
    text_update_mode: Literal[settings.TEXT_UPDATE_MODES] = "onBlur"
    triggers: List[Any] = []


QUESTION_TYPES = [
    BarRatingQuestion,
    BooleanQuestion,
    BootstrapDatePickerQuestion,
    BootstrapSliderQuestion,
    CheckboxQuestion,
    CKEditorQuestion,
    CommentQuestion,
    DropdownQuestion,
    EmotionsRatingQuestion,
    FileQuestion,
    ImagePickerQuestion,
    JQueryUIDatePickerQuestion,
    MatrixDropdownQuestion,
    MatrixDynamicQuestion,
    MatrixQuestion,
    MicrophoneQuestion,
    MultipleTextQuestion,
    NoUISliderQuestion,
    RadioGroupQuestion,
    RatingQuestion,
    Select2Question,
    SignaturePadQuestion,
    SortableJSQuestion,
    TagBoxQuestion,
    TextQuestion,
]


QUESTION_NAMES_TO_TYPES = {
    "barrating": BarRatingQuestion,
    "boolean": BooleanQuestion,
    "bootstrapdatepicker": BootstrapDatePickerQuestion,
    "bootstrapslider": BootstrapSliderQuestion,
    "checkbox": CheckboxQuestion,
    "editor": CKEditorQuestion,
    "comment": CommentQuestion,
    "dropdown": DropdownQuestion,
    "emotionsratings": EmotionsRatingQuestion,
    "expression": ExpressionBlock,
    "file": FileQuestion,
    "html": HtmlBlock,
    "image": ImageBlock,
    "imagepicker": ImagePickerQuestion,
    "datepicker": JQueryUIDatePickerQuestion,
    "matrixdropdown": MatrixDropdownQuestion,
    "matrixdynamic": MatrixDynamicQuestion,
    "matrix": MatrixQuestion,
    "microphone": MicrophoneQuestion,
    "multipletext": MultipleTextQuestion,
    "nouislider": NoUISliderQuestion,
    "radiogroup": RadioGroupQuestion,
    "rating": RatingQuestion,
    "select2": Select2Question,
    "signaturepad": SignaturePadQuestion,
    "sortablelist": SortableJSQuestion,
    "tagbox": TagBoxQuestion,
    "text": TextQuestion,
}
