from dialog_api import messaging_pb2
from google.protobuf import wrappers_pb2


class InteractiveMediaButton(object):
    """Button control class.

    """
    def __init__(self, value, label=None):
        self.value = value
        self.label = label

    def render(self, target):
        """Render method for button

        :param target: target button
        """
        if self.label is not None:
            target.label.value = self.label
        target.value = self.value


class InteractiveMediaSelect(object):
    """Select control class.

    """
    def __init__(self, label=None, default_value=None, options=None):
        assert options is not None
        self.label = label
        self.default_value = default_value
        self.options = options

    def render(self, target):
        """Render method for select

        :param target: target select
        """
        if self.label is not None:
            target.label.value = self.label
        if self.default_value is not None:
            target.default_value.value = self.default_value
        for value, label in self.options.iteritems():
            opt = target.options.add()
            opt.value = value
            opt.label = label


class InteractiveMediaConfirm(object):
    """Confirm control class.

    """
    def __init__(self, text=None, title=None, ok=None, dismiss=None):
        self.text = text
        self.title = title
        self.ok = ok
        self.dismiss = dismiss

    def render(self):
        """Render method for confirm

        :return: confirm
        """
        confirm = messaging_pb2.InteractiveMediaConfirm()
        if self.text is not None:
            confirm.text = wrappers_pb2.StringValue(value=self.text)
        if self.title is not None:
            confirm.title = wrappers_pb2.StringValue(value=self.title)
        if self.ok is not None:
            confirm.ok = wrappers_pb2.StringValue(value=self.ok)
        if self.dismiss is not None:
            confirm.dismiss = wrappers_pb2.StringValue(value=self.dismiss)
        return confirm


class InteractiveMedia(object):
    """Wrapper class for interactive object styling.

    """
    style_map = {
        'default': messaging_pb2.INTERACTIVEMEDIASTYLE_DEFAULT,
        'primary': messaging_pb2.INTERACTIVEMEDIASTYLE_PRIMARY,
        'danger': messaging_pb2.INTERACTIVEMEDIASTYLE_DANGER
    }
    # style one of ['default', 'primary', 'danger', None]
    # widget = InteractiveMediaButton | InteractiveMediaSelect

    def __init__(self, id, widget, style=None, confirm=None):
        self.id = id
        self.widget = widget
        self.style = style
        self.confirm = confirm

    def render(self, target):
        """Render method for wrapped interactive object.

        :param target: target interactive object
        :return: wrapped interactive object
        """
        target.id = str(self.id)
        target.style = self.style_map.get(self.style, messaging_pb2.INTERACTIVEMEDIASTYLE_UNKNOWN)
        if self.widget is not None:
            if isinstance(self.widget, InteractiveMediaButton):
                self.widget.render(target.widget.interactiveMediaButton)
            elif isinstance(self.widget, InteractiveMediaSelect):
                self.widget.render(target.widget.interactiveMediaSelect)
        if self.confirm is not None:
            target.confirm = self.confirm.render()
        return target


class InteractiveMediaGroup(object):
    """Wrapper class for interactive object grouping.

    """
    # translations = {'lang': [{'id': 'value'}]} dict
    def __init__(self, actions, title=None, description=None, translations=None):
        assert isinstance(actions, list)
        self.actions = actions
        self.title = title
        self.description = description
        self.translations = translations

    def render(self, target):
        """Render method for group of interactive objects.

        :param target: group of interactive objects
        """
        media = target.actions.add()
        for action in self.actions:
            act = media.actions.add()
            action.render(act)
        if self.title is not None:
            media.title.value = self.title
        if self.description is not None:
            media.description.value = self.description
        for lang, trans in self.translations.items():
            group = messaging_pb2.InteractiveMediaTranslationGroup(lang=lang)
            for idx, value in trans.items():
                group.messages.append(messaging_pb2.InteractiveMediaTranslation(id=idx, value=value))
            media.translations.append(group)