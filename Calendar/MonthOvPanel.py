from PanelDesign import PanelDesign
from Assets import colors
from settings import general_settings, week_starts_on
import calendar as callib
from datetime import datetime, timedelta
from WeatherHeaderDesign import WeatherHeaderDesign
from PIL import ImageDraw
from TextDesign import TextDesign
from BoxDesign import BoxDesign
from EllipseDesign import EllipseDesign
from MonthBlockDesign import MonthBlockDesign, daynumberboxsize
from EventListDesign import EventListDesign
from RssPostListDesign import RssPostListDesign
from settings import general_settings
from CryptoListDesign import CryptoListDesign


weatherheadersize = (1, 0.113)
monthboxsize = (1, 0.085)
monthtextsize = monthboxsize[1] * 0.75
monthplace = (0, 0.11 - weatherheadersize[1])
monthovsize = (1, 0.48)
monthovposition = (0, 0.25 - weatherheadersize[1])
seperatorplace = (0, 0.113)
weekdayrowpos = (0, 0.209 - weatherheadersize[1])
weekrowboxsize = (1, 0.044)
weekdaytextsize = 0.7 * weekrowboxsize[1]
weekdaytextpadding = -0.001
weekrownameboxsize = (0.143, 0.044)
eventcirclehorizontalsize = 0.100


class MonthOvPanel (PanelDesign):
    """Overview that focuses on the current month and
    some additional information in the bottom."""

    def __init__(self, size):
        super(MonthOvPanel, self).__init__(size)
        self.weather_header_height = 0
        if general_settings["weather-info"]:
            self.weather_header_height = self.size[1] * weatherheadersize[1]
        self.__first_render__()

    def __first_render__(self):
        if week_starts_on == "Monday":
            callib.setfirstweekday(callib.MONDAY)
        elif week_starts_on == "Sunday":
            callib.setfirstweekday(callib.SUNDAY)
        self.__week_days__ = self.__get_week_days_ordered__()

        self.__draw_month_name__()
        self.__draw_week_row__()

        if general_settings["weather-info"]:
            self.__draw_seperator__()

        self.month_block = MonthBlockDesign(self.__abs_pos__(
            monthovsize), datetime.now(), highlight_today=True)
        pos = self.__abs_pos__(monthovposition)
        pos = (pos[0], pos[1] + self.weather_header_height)
        self.month_block.pos = pos
        self.draw_design(self.month_block)

    def add_weather(self, weather):
        if general_settings["weather-info"] == False:
            return
        self.draw_design(WeatherHeaderDesign(
            self.__abs_pos__(weatherheadersize), weather))

    def add_rssfeed(self, rss):
        if general_settings["info-area"] is "rss":
            self.__draw_rss_post_list_to_bottom__(rss)

    def add_crypto(self, crypto):
        if general_settings["info-area"] is "crypto":
            self.__draw_crypto_post_list_to_bottom__(crypto)

    def add_tasks(self, tasks):
        pass

    def add_calendar(self, calendar):
        if general_settings["highlight-event-days"]:
            month_events = list(set([(event.begin_datetime.day, event.begin_datetime.month,
                                      event.begin_datetime.year) for event in calendar.get_month_events()]))
            for event in month_events:
                self.__draw_highlight_event_day__(event)

        if general_settings["info-area"] is "events":
            self.__draw_event_list_to_bottom__(calendar)

    def __draw_rss_post_list_to_bottom__(self, rss):
        month_pos = self.__abs_pos__(monthovposition)
        month_height = self.month_block.get_real_height()
        size = (self.size[0], self.size[1] - (month_pos[1] +
                                              month_height + self.weather_header_height))
        info_list = RssPostListDesign(size, rss)
        info_list.pos = (
            int(month_pos[0]), month_pos[1] + month_height + self.weather_header_height)
        self.draw_design(info_list)

    def __draw_crypto_post_list_to_bottom__(self, crypto):
        month_pos = self.__abs_pos__(monthovposition)
        month_height = self.month_block.get_real_height()
        size = (self.size[0], self.size[1] - (month_pos[1] +
                                              month_height + self.weather_header_height))

        info_list = CryptoListDesign(size, crypto)
        list_height = info_list.get_estimated_height()
        info_list.pos = (int(month_pos[0]), month_pos[1] + month_height +
                         self.weather_header_height + (size[1] - list_height))
        self.draw_design(info_list)

    def __draw_event_list_to_bottom__(self, calendar):
        month_pos = self.__abs_pos__(monthovposition)
        month_height = self.month_block.get_real_height()
        size = (self.size[0], self.size[1] - (month_pos[1] +
                                              month_height + self.weather_header_height))

        events = calendar.get_upcoming_events()
        info_list = EventListDesign(size, events)
        info_list.pos = (int(month_pos[0]), int(
            month_pos[1] + month_height + self.weather_header_height))
        self.draw_design(info_list)

    def __draw_highlight_event_day__(self, date):
        first_month_week = datetime(date[2], date[1], 1).isocalendar()[1]
        cur_date = datetime(date[2], date[1], date[0])

        side_length = int(eventcirclehorizontalsize * self.size[0])
        circle_size = (side_length, side_length)
        pos = self.month_block.get_day_pos(cur_date.isocalendar(
        )[1] - first_month_week, self.__get_day_of_week__(cur_date), rel_pos=self.month_block.pos)
        place_size = (self.month_block.size[0] * daynumberboxsize[0],
                      self.month_block.size[1] * daynumberboxsize[1])
        pos = (int(pos[0] + (place_size[0] - circle_size[0]) / 2),
               int(pos[1] + (place_size[1] - circle_size[1]) / 2))
        self.__draw_highlight_circle__(circle_size, pos, 'red', width=2)

    def __abs_pos__(self, pos, size=None):
        if size is None:
            size = self.size
        return (int(pos[0] * size[0]), int(pos[1] * size[1]))

    def __draw_seperator__(self):
        """Draw a line seperating the weather and Calendar section"""
        ImageDraw.Draw(self.__image__).line([self.__abs_pos__(
            seperatorplace), self.__abs_pos__((1, seperatorplace[1]))], fill='red', width=5)

    def __draw_month_name__(self):
        """Draw the icon with the current month's name"""
        month = datetime.now().strftime("%B")
        txt = TextDesign(self.__abs_pos__(monthboxsize), fontsize=monthtextsize *
                         self.size[1], text=month, verticalalignment="center", horizontalalignment="center")
        pos = self.__abs_pos__(monthplace)
        txt.pos = (pos[0], pos[1] + self.weather_header_height)
        self.draw_design(txt)

    def __draw_week_row__(self):
        for day_of_week, day in enumerate(self.__week_days__):
            txt = TextDesign(self.__abs_pos__(weekrownameboxsize), fontsize=weekdaytextsize *
                             self.size[1], text=str(day), verticalalignment="center", horizontalalignment="center")
            pos = self.__get_week_day_pos__(day_of_week)
            txt.pos = (pos[0], pos[1] + weekdaytextpadding * self.size[1])
            self.draw_design(txt)

        self.__draw_highlight_box__(self.__abs_pos__(weekrownameboxsize), self.__get_week_day_pos__(
            self.__get_day_of_week__(datetime.now())), width=1)

    def __get_week_day_pos__(self, day_of_week):
        maxwidth, _ = self.__abs_pos__(monthovsize)
        partialwidth = maxwidth / 7
        posx, posy = self.__abs_pos__(weekdayrowpos)
        return (int(posx + day_of_week * partialwidth), int(posy + self.weather_header_height))

    def __draw_highlight_box__(self, size, pos, color=colors["fg"], width=1):
        design = BoxDesign(size, outline=color, width=width)
        design.pos = pos
        self.draw_design(design)

    def __draw_highlight_circle__(self, size, pos, color=colors["fg"], width=1):
        design = EllipseDesign(size, outline=color, width=width)
        design.pos = pos
        self.draw_design(design)

    def __get_week_days_ordered__(self):
        cur_weekday = datetime.now().weekday()
        correction = -cur_weekday
        if week_starts_on == "Sunday":
            correction -= 1

        weekdays = []
        for i in range(7):
            weekdays.append(
                (datetime.now() + timedelta(days=(i + correction))).strftime("%a"))

        return weekdays

    def __get_day_of_week__(self, date):
        return self.__week_days__.index(date.strftime("%a"))
