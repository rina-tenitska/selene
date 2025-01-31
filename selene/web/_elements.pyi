from __future__ import annotations

from types import MappingProxyType

from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import (
    Callable,
    Iterable,
    Optional,
    Tuple,
    TypeVar,
    Union,
    Any,
    Generic,
    Dict,
    Literal,
    cast,
)
import typing_extensions as typing
from selene.core.condition import Condition
from selene.core.configuration import Config
from selene.core.entity import WaitingEntity, Assertable
from selene.core.locator import Locator
from selene.core.wait import Wait

E = TypeVar('E', bound='Assertable')
R = TypeVar('R')

@typing.runtime_checkable
class _SearchContext(typing.Protocol):
    def find_element(self, by: str, value: str | None = None) -> WebElement: ...
    def find_elements(
        self, by: str, value: str | None = None
    ) -> typing.List[WebElement]: ...

class _ElementsContext(WaitingEntity['_ElementsContext']):
    """An Element-like class that serves as pure context for search elements inside
    via `element(selector_or_by)` or `all(selector_or_by)` methods"""

    def __init__(self, locator: Locator[_SearchContext], config: Config): ...

    # --- Configured --- #

    def with_(
        self, config: Optional[Config] = None, **config_as_kwargs
    ) -> _ElementsContext: ...

    # --- Located --- #

    def __str__(self): ...
    def locate(self) -> _SearchContext: ...
    @property
    def __raw__(self) -> _SearchContext: ...
    def __call__(self) -> _SearchContext: ...

    # --- WaitingEntity --- #

    @property
    def wait(self) -> Wait[_ElementsContext]: ...
    @property
    def cached(self) -> _ElementsContext: ...

    # --- Relative location --- #

    def element(self, selector_or_by: Union[str, Tuple[str, str]], /) -> Element:
        by = self.config._selector_or_by_to_by(selector_or_by)

        return Element(
            Locator(f'{self}.element({by})', lambda: self().find_element(*by)),
            self.config,
        )

    def all(self, selector_or_by: Union[str, Tuple[str, str]], /) -> Collection:
        by = self.config._selector_or_by_to_by(selector_or_by)

        return Collection(
            Locator(f'{self}.all({by})', lambda: self().find_elements(*by)),
            self.config,
        )

class Element(WaitingEntity['Element']):
    def __init__(self, locator: Locator[WebElement], config: Config) -> None: ...
    def with_(
        self,
        config: Optional[Config] = None,
        *,
        # Options to customize general Selene behavior
        # > to customize waiting logic
        timeout: float = 4,
        # poll_during_waits: int = ...,  # currently fake option
        # _wait_decorator: Callable[[Wait[E]], Callable[[F], F]] = lambda w: lambda f: f,
        # reports_folder: Optional[str] = ...,
        # _counter: itertools.count = ...,
        save_screenshot_on_failure: bool = True,
        save_page_source_on_failure: bool = True,
        # last_screenshot: Optional[str] = None,
        # last_page_source: Optional[str] = None,
        # _save_screenshot_strategy: Callable[[Config, Optional[str]], Any] = ...,
        # _save_page_source_strategy: Callable[[Config, Optional[str]], Any] = ...,
        # # Options to customize web browser and elements behavior
        # base_url: str = '',
        # _get_base_url_on_open_with_no_args: bool = False,
        # window_width: Optional[int] = None,
        # window_height: Optional[int] = None,
        log_outer_html_on_failure: bool = False,
        set_value_by_js: bool = False,
        type_by_js: bool = False,
        click_by_js: bool = False,
        wait_for_no_overlap_found_by_js: bool = False,
        _match_only_visible_elements_texts: bool = True,
        _match_only_visible_elements_size: bool = False,
        _match_ignoring_case: bool = False,
        _placeholders_to_match_elements: Dict[
            Literal['exactly_one', 'zero_or_one', 'one_or_more', 'zero_or_more'], Any
        ] = cast(  # noqa
            dict, MappingProxyType({})
        ),
        selector_to_by_strategy: Callable[[str], Tuple[str, str]] = ...,
        # Etc.
        _build_wait_strategy: Callable[[Config], Callable[[E], Wait[E]]] = ...,
    ) -> Element: ...
    def locate(self) -> WebElement: ...
    @property
    def __raw__(self): ...
    def __call__(self) -> WebElement: ...
    @property
    def wait(self) -> Wait[Element]: ...
    @property
    def cached(self) -> Element: ...
    def element(self, css_or_xpath_or_by: Union[str, Tuple[str, str]]) -> Element: ...
    def all(self, css_or_xpath_or_by: Union[str, Tuple[str, str]]) -> Collection: ...
    @property
    def shadow_root(self) -> _ElementsContext: ...
    @property
    def frame_context(self) -> _FrameContext: ...
    def execute_script(self, script_on_self: str, *arguments): ...
    def set_value(self, value: Union[str, int]) -> Element: ...
    def set(self, value: Union[str, int]) -> Element: ...
    def type(self, text: Union[str, int]) -> Element: ...
    def send_keys(self, *value) -> Element: ...
    def press(self, *keys) -> Element: ...
    def press_enter(self) -> Element: ...
    def press_escape(self) -> Element: ...
    def press_tab(self) -> Element: ...
    def clear(self) -> Element: ...
    def submit(self) -> Element: ...
    def click(self, *, xoffset=0, yoffset=0) -> Element: ...
    def double_click(self) -> Element: ...
    def context_click(self) -> Element: ...
    def hover(self) -> Element: ...
    def s(self, css_or_xpath_or_by: Union[str, Tuple[str, str]]) -> Element: ...
    def ss(self, css_or_xpath_or_by: Union[str, Tuple[str, str]]) -> Collection: ...

class Collection(WaitingEntity['Collection'], Iterable[Element]):
    def __init__(
        self, locator: Locator[typing.Sequence[WebElement]], config: Config
    ) -> None: ...
    def with_(
        self,
        config: Optional[Config] = None,
        *,
        # Options to customize general Selene behavior
        # > to customize waiting logic
        timeout: float = 4,
        poll_during_waits: int = ...,  # currently fake option
        # _wait_decorator: Callable[[Wait[E]], Callable[[F], F]] = lambda w: lambda f: f,
        # reports_folder: Optional[str] = ...,
        # _counter: itertools.count = ...,
        save_screenshot_on_failure: bool = True,
        save_page_source_on_failure: bool = True,
        # last_screenshot: Optional[str] = None,
        # last_page_source: Optional[str] = None,
        # _save_screenshot_strategy: Callable[[Config, Optional[str]], Any] = ...,
        # _save_page_source_strategy: Callable[[Config, Optional[str]], Any] = ...,
        # # Options to customize web browser and elements behavior
        # base_url: str = '',
        # _get_base_url_on_open_with_no_args: bool = False,
        # window_width: Optional[int] = None,
        # window_height: Optional[int] = None,
        log_outer_html_on_failure: bool = False,
        set_value_by_js: bool = False,
        type_by_js: bool = False,
        click_by_js: bool = False,
        wait_for_no_overlap_found_by_js: bool = False,
        _match_only_visible_elements_texts: bool = True,
        _match_only_visible_elements_size: bool = False,
        _match_ignoring_case: bool = False,
        _placeholders_to_match_elements: Dict[
            Literal['exactly_one', 'zero_or_one', 'one_or_more', 'zero_or_more'], Any
        ] = cast(  # noqa
            dict, MappingProxyType({})
        ),
        selector_to_by_strategy: Callable[[str], Tuple[str, str]] = ...,
        # Etc.
        _build_wait_strategy: Callable[[Config], Callable[[E], Wait[E]]] = ...,
    ) -> Collection: ...
    def locate(self) -> typing.Sequence[WebElement]: ...
    @property
    def __raw__(self): ...
    def __call__(self) -> typing.Sequence[WebElement]: ...
    @property
    def cached(self) -> Collection: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def element(self, index: int) -> Element: ...
    @property
    def first(self) -> Element: ...
    @property
    def second(self) -> Element: ...
    @property
    def even(self): ...
    @property
    def odd(self): ...
    def sliced(
        self, start: Optional[int] = ..., stop: Optional[int] = ..., step: int = ...
    ) -> Collection: ...
    def __getitem__(
        self, index_or_slice: Union[int, slice]
    ) -> Union[Element, Collection]: ...
    def from_(self, start: int) -> Collection: ...
    def to(self, stop: int) -> Collection: ...
    def by(
        self, condition: Union[Condition[Element], Callable[[Element], None]]
    ) -> Collection: ...
    def filtered_by(
        self, condition: Union[Condition[Element], Callable[[Element], None]]
    ) -> Collection: ...
    def by_their(
        self,
        selector: Union[str, Tuple[str, str], Callable[[Element], Element]],
        condition: Condition[Element],
    ) -> Collection: ...
    def element_by(
        self, condition: Union[Condition[Element], Callable[[Element], None]]
    ) -> Element: ...
    def element_by_its(
        self,
        selector: Union[str, Tuple[str, str], Callable[[Element], Element]],
        condition: Condition[Element],
    ) -> Element: ...
    def collected(
        self, finder: Callable[[Element], Union[Element, Collection]]
    ) -> Collection: ...
    def all(self, selector: Union[str, Tuple[str, str]]) -> Collection: ...
    def all_first(self, selector: Union[str, Tuple[str, str]]) -> Collection: ...
    # --- Unique for Web --- #
    @property
    def shadow_roots(self) -> Collection: ...

AllElements = Collection
All = AllElements

class _FrameContext:
    def __init__(self, element: Element): ...
    def decorator(self, func): ...

    # aliases :) TODO: not sure which to keep
    def _step(self, func): ...
    def _steps(self, func): ...
    def _content(self, func): ...
    def _inside(self, func): ...
    def _inner(self, func): ...
    def within(self, func): ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...
    @property
    def __as_wait_decorator(self): ...
    def element(self, selector: str | typing.Tuple[str, str]) -> Element: ...
    def all(self, selector: str | typing.Tuple[str, str]) -> Collection: ...
