import datetime


class Activity:
    def __init__(self):
        self.startTime = datetime.datetime.now()

    def close(self, _):
        pass

    def dump_if_too_long(self, activity_accumulator):
        if datetime.datetime.now() - self.startTime >= datetime.timedelta(minutes=5):
            self.close(activity_accumulator)


class AppWork(Activity):
    def __init__(self, app_name, title):
        Activity.__init__(self)
        self.appName = app_name
        self.titles = set()
        self.titles.add(title)

    def on_timer(self, idle, app_name, title, activity_accumulator):
        if idle or app_name != self.appName:
            self.close(activity_accumulator)
            return IdleAction() if idle else get_activity(app_name, title)
        else:
            self.titles.add(title)
            self.dump_if_too_long(activity_accumulator)
            return self

    def close(self, activity_accumulator):
        titles = '| '.join(self.titles)
        activity_accumulator.add_new_activity(self.appName, titles, self.startTime,
                                              datetime.datetime.now())
        self.titles.clear()
        self.startTime = datetime.datetime.now()


###############################################################################
class IdleAction(Activity):
    def __init__(self):
        Activity.__init__(self)

    def on_timer(self, idle, app_name, title, activity_accumulator):
        if not idle:
            self.close(activity_accumulator)
            assert(len(app_name))
            return get_activity(app_name, title)
        else:
            self.dump_if_too_long(activity_accumulator)
            return self

    def close(self, activity_accumulator):
        activity_accumulator.add_new_activity('<away>', '', self.startTime,
                                              datetime.datetime.now())
        self.startTime = datetime.datetime.now()


def get_activity(app_name, title):
    assert(len(app_name) and app_name[-3] != 'exe')
    return AppWork(app_name, title)


def main():
    pass


if __name__ == '__main__':
    main()
