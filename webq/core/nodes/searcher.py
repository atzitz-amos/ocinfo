import abc


class HTMLSearchConditions:
    class Matcher(abc.ABC):
        def match(self, component):
            """ Return None if not matched, otherwise return list of matched nodes """
            raise NotImplementedError

    class OneOfMatcher(Matcher):
        def __init__(self, matchers):
            self.matchers = matchers

        def match(self, component):
            result = []
            for matcher in self.matchers:
                if (c := matcher.match(component)) is not None:
                    result.extend(c)
            return result

    class AllOfMatcher(Matcher):
        def __init__(self, matchers):
            self.matchers = matchers

        def match(self, component):
            result = []
            for matcher in self.matchers:
                if (c := matcher.match(component)) is None:
                    return None
                for i in c:  # basically set intersection
                    if i not in result:
                        result.append(i)
                for i in result:
                    if i not in c:
                        result.remove(i)
            return result

    class DirectChildMatcher(Matcher):
        def __init__(self, matcher):
            self.matcher = matcher

        def match(self, component):
            result = []
            for child in component.children:
                if (c := self.matcher.match(child)) is not None:
                    result.extend(c)
            return result or None

    class ChildMatcher(Matcher):
        def __init__(self, matcher):
            self.matcher = matcher

        def match(self, component):
            result = []
            for child in component.children:
                if (c := self.matcher.match(child)) is not None:
                    result.extend(c)
                if c := self.match(child):
                    result.extend(c)
            return result

    class FirstAfterMatcher(Matcher):
        def __init__(self, matcher):
            self.matcher = matcher

        def match(self, component):
            if not component.parent:
                return None
            i = 0
            while i < len(component.parent.children):
                if component.parent.children[i] == component:
                    break
                i += 1

            result = []
            while i < len(component.parent.children):
                if (c := self.matcher.match(component.parent.children[i])) is not None:
                    result.extend(c)
                i += 1
            return result

    class PrecedingMatcher(Matcher):
        def __init__(self, matcher):
            self.matcher = matcher

        def match(self, component):
            if not component.parent:
                return None
            i = 0
            while i < len(component.parent.children):
                if component.parent.children[i] == component:
                    break
                i += 1

            while i >= 0:
                if self.matcher.match(component.parent.children[i]) is not None:
                    return [component]
                i -= 1
            return None

    class HasMatcher(Matcher):
        def __init__(self, matcher):
            self.matcher = matcher

        def match(self, component):
            if self.matcher.match(component) is not None:
                return [component]
            return None

    class NotMatcher(Matcher):
        def __init__(self, matcher):
            self.matcher = matcher

        def match(self, component):
            if self.matcher.match(component) is None:
                return [component]
            return None

    class Condition(Matcher):
        def check(self, component):
            """ Return True if matched, otherwise return False """
            raise NotImplementedError

        def match(self, component):
            return [component] if self.check(component) else None

    class IDCondition(Condition):
        def __init__(self, id_):
            self.id = id_

        def check(self, component):
            return component.attributes.get("id") == self.id

    class ClassCondition(Condition):
        def __init__(self, class_):
            self.class_ = class_

        def check(self, component):
            return self.class_ in component.attributes.get("class", "").split()

    class TagCondition(Condition):
        def __init__(self, tag):
            self.tag = tag

        def check(self, component):
            return hasattr(component, "tagname") and component.tagname == self.tag

    class AttributeCondition(Condition):
        def __init__(self, key, value, op):
            self.key = key
            self.value = value
            self.op = op

        def check(self, component):
            match self.op:
                case "":
                    return component.attributes.get(self.key) is not None
                case "=":
                    return component.attributes.get(self.key) == self.value
                case "~=":
                    return self.value in component.attributes.get(self.key, "").split()
                case "|=":
                    return component.attributes.get(self.key, "").split("-") == self.value
                case "^=":
                    return component.attributes.get(self.key, "").startswith(self.value)
                case "$=":
                    return component.attributes.get(self.key, "").endswith(self.value)
                case "*=":
                    return self.value in component.attributes.get(self.key, "")
                case _:
                    raise ValueError(f"Invalid operator: {self.op}")

    class NthChildCondition(Condition):
        def __init__(self, n):
            self.n = n - 1

        def check(self, component):
            return component.parent and self.n < len(component.parent.children) and component.parent.children[self.n] == component

    class NthOfTypeCondition(Condition):
        def __init__(self, n):
            self.n = n - 1

        def check(self, component):
            if not component.parent:
                return False
            i = 0
            for child in component.parent.children:
                if child.tagname == component.tagname:
                    if i == self.n:
                        return True
                    i += 1
            return None

    class NthLastChildCondition(Condition):
        def __init__(self, n):
            self.n = n

        def check(self, component):
            return component.parent and self.n >= len(component.parent.children) and component.parent.children[-self.n] == component

    class NthLastOfTypeCondition(Condition):
        def __init__(self, n):
            self.n = n - 1

        def check(self, component):
            if not component.parent:
                return False
            i = 0
            for child in reversed(component.parent.children):
                if child.tagname == component.tagname:
                    if child == component and i == self.n:
                        return True
                    elif i == self.n or child == component:
                        return False
                    i += 1
            return False

    class FirstChildCondition(NthChildCondition):
        def __init__(self):
            super().__init__(1)

    class FirstOfTypeCondition(NthOfTypeCondition):
        def __init__(self):
            super().__init__(1)

    class LastChildCondition(NthLastChildCondition):
        def __init__(self):
            super().__init__(1)

    class LastOfTypeCondition(NthLastOfTypeCondition):
        def __init__(self):
            super().__init__(1)

    class OnlyOfTypeCondition(Condition):
        def check(self, component):
            if not component.parent:
                return False
            for child in component.parent.children:
                if child.tagname == component.tagname and child != component:
                    return False
            return True

    class OnlyChildCondition(Condition):
        def check(self, component):
            return not component.parent or len(component.parent.children) == 1

    class AlwaysTrueCondition(Condition):
        def check(self, component):
            return True

    PSEUDO_ELEMENTS_MAPPING = {
        "first-child": FirstChildCondition,
        "last-child": LastChildCondition,
        "first-of-type": FirstOfTypeCondition,
        "last-of-type": LastOfTypeCondition,
        "only-child": OnlyChildCondition,
        "only-of-type": OnlyOfTypeCondition,
        "nth-child": NthChildCondition,
        "nth-last-child": NthLastChildCondition,
        "nth-of-type": NthOfTypeCondition,
        "nth-last-of-type": NthLastOfTypeCondition,
        "has": HasMatcher,
        "not": NotMatcher
    }


class HTMLSearchQueryParser:
    SEPARATORS = ",>+~ "
    _CACHE = {}

    __slots__ = ("q", "i")

    def __init__(self, q):
        self.q = q

        self.i = 0

    def parse(self):
        if self.q in self._CACHE:
            return self._CACHE[self.q]

        if self.q[self.i] not in self.SEPARATORS:
            result = [self.parsePart()]
        else:
            result = []
        current = []
        while self.i < len(self.q):
            self.i += 1
            if self.q[self.i - 1] == " " and self.q[self.i] in self.SEPARATORS:
                sep = " "
                while self.q[self.i] in self.SEPARATORS:
                    if self.q[self.i] != " ":
                        sep = self.q[self.i]
                    self.i += 1
            else:
                sep = self.q[self.i - 1]
            match sep:
                case ",":
                    current.append(self.parsePart())
                case ">":
                    if current:
                        result.append(HTMLSearchConditions.OneOfMatcher(current))
                        current = []
                    result.append(HTMLSearchConditions.DirectChildMatcher(self.parsePart()))
                case "+":
                    if current:
                        result.append(HTMLSearchConditions.OneOfMatcher(current))
                        current = []
                    result.append(HTMLSearchConditions.FirstAfterMatcher(self.parsePart()))
                case "~":
                    if current:
                        result.append(HTMLSearchConditions.OneOfMatcher(current))
                        current = []
                    result.append(HTMLSearchConditions.PrecedingMatcher(self.parsePart()))
                case " ":
                    if current:
                        result.append(HTMLSearchConditions.OneOfMatcher(current))
                        current = []
                    result.append(HTMLSearchConditions.ChildMatcher(self.parsePart()))
                case ":":
                    current.append(self.parsePseudo(result[-1] if result else None))
                    result.append(self.parsePseudo(result[-1] if result else None))
                case ")":
                    break
                case _:
                    raise ValueError(f"Invalid character: {self.q[self.i - 1]}")
        if current:
            result.append(HTMLSearchConditions.OneOfMatcher(current))
        result = HTMLSearchConditions.AllOfMatcher(result) if len(result) > 1 else result[0]
        self._CACHE[self.q] = result
        return result

    def parsePart(self):
        result = self._parsePart()
        return HTMLSearchConditions.AllOfMatcher(result) if len(result) != 1 else result[0]

    def _parsePart(self):
        self._eliminate_spaces()
        if len(self.q) <= self.i:
            return []
        part = self.q[self.i]
        typ = HTMLSearchConditions.TagCondition
        if part == "#":
            typ = HTMLSearchConditions.IDCondition
        elif part == ".":
            typ = HTMLSearchConditions.ClassCondition
        elif part == "[":
            return [self.parseAttribute(), *self._parsePart()]
        elif part == "*":
            self.i += 1
            return [HTMLSearchConditions.AlwaysTrueCondition(), *self._parsePart()]
        elif part == ":":
            self.i += 1
            return [self.parsePseudo(None), *self._parsePart()]
        result = []
        bundle = ""
        while self.i < len(self.q) and self.q[self.i] not in self.SEPARATORS and self.q[self.i] != ")":
            if self.q[self.i] in "#.[:":
                if bundle: result.append(typ(bundle))
                bundle = ""
                part = self.q[self.i]
                if part == "#":
                    typ = HTMLSearchConditions.IDCondition
                elif part == ".":
                    typ = HTMLSearchConditions.ClassCondition
                elif part == "[":
                    result.append(self.parseAttribute())
                elif part == "*":
                    self.i += 1
                    return HTMLSearchConditions.AlwaysTrueCondition()
                elif part == ":":
                    self.i += 1
                    result.append(self.parsePseudo(None))
                else:
                    typ = HTMLSearchConditions.TagCondition
            else:
                bundle += self.q[self.i]
            self.i += 1
        if bundle: result.append(typ(bundle))
        return result

    def parseAttribute(self):
        self.i += 1
        key = ""
        while self.q[self.i] not in "=~|^$* ]":
            if self.i >= len(self.q):
                raise ValueError("Missing closing bracket")
            key += self.q[self.i]
            self.i += 1
        self._eliminate_spaces()
        match self.q[self.i]:
            case "]":
                self.i += 1
                return HTMLSearchConditions.AttributeCondition(key, "", "")
            case "=":
                op = "="
            case "~":
                op = "~="
                if self.i + 1 < len(self.q) and self.q[self.i + 1] != "=":
                    raise ValueError("Invalid operator")
                self.i += 1
            case "|":
                op = "|="
                if self.i + 1 < len(self.q) and self.q[self.i + 1] != "=":
                    raise ValueError("Invalid operator")
                self.i += 1
            case "^":
                op = "^="
                if self.i + 1 < len(self.q) and self.q[self.i + 1] != "=":
                    raise ValueError("Invalid operator")
                self.i += 1
            case "$":
                op = "$="
                if self.i + 1 < len(self.q) and self.q[self.i + 1] != "=":
                    raise ValueError("Invalid operator")
                self.i += 1
            case "*":
                op = "*="
                if self.i + 1 < len(self.q) and self.q[self.i + 1] != "=":
                    raise ValueError("Invalid operator")
                self.i += 1
            case _:
                raise ValueError("Invalid operator")
        self.i += 1
        self._eliminate_spaces()
        value = ""
        while self.q[self.i] != "]":
            if self.i >= len(self.q):
                raise ValueError("Missing closing bracket")
            value += self.q[self.i]
            self.i += 1
        self.i += 1
        return HTMLSearchConditions.AttributeCondition(key, value, op)

    def parsePseudo(self, element):
        is_pseudo_element = False
        if self.q[self.i] == ":":
            self.i += 1
            is_pseudo_element = True
        key = ""
        while self.i < len(self.q) and self.q[self.i] not in self.SEPARATORS + "(":
            key += self.q[self.i]
            self.i += 1
        return self.parsePseudoElement(element, key) if is_pseudo_element else self.parsePseudoFunction(element, key)

    def parsePseudoElement(self, element, key):
        """ TODO """

    def parsePseudoFunction(self, element, key):
        def parseArgs():
            initial = self.i + 1
            final = self.q.index(")", initial)
            self.i = final
            return self.q[initial:final]

        if key in ("defined", "active", "hover", "focus", "popover-open", "enabled", "disabled", "checked", "indeterminate", "valid", "invalid", "required", "optional", "read-only", "read-write", "modal", "playing", "paused", "seeking", "buffering", "stalled", "muted", "volume-locked", "in-range", "out-of-range", "autofill"):
            result = None
        elif key in ("not", "has"):
            self.i += 1
            result = HTMLSearchConditions.PSEUDO_ELEMENTS_MAPPING[key](self.parse())
            self.i += 1
        elif key in ("nth-child", "nth-last-child", "nth-of-type", "nth-last-of-type"):
            result = HTMLSearchConditions.PSEUDO_ELEMENTS_MAPPING[key](int(parseArgs()))
        elif key in ("first-child", "last-child", "only-child", "first-of-type", "last-of-type", "only-of-type"):
            result = HTMLSearchConditions.PSEUDO_ELEMENTS_MAPPING[key]()
        elif key == "lang":
            result = HTMLSearchConditions.AttributeCondition("lang", parseArgs(), "=")
        else:
            raise ValueError(f"Invalid pseudo function: {key}")

        return result

    def _eliminate_spaces(self):
        while len(self.q) > self.i and self.q[self.i] == " ":
            self.i += 1


class HTMLSearcher:

    def __init__(self, component):
        self.component = component

    def find_all(self, q):
        viewed = set()
        query = HTMLSearchQueryParser(q).parse()
        for component in self.component.iterators().linear():
            if query.match(component) and component not in viewed:
                yield component
                viewed.add(component)

    def find_one(self, q):
        query = HTMLSearchQueryParser(q).parse()
        for component in self.component.iterators().linear():
            if query.match(component):
                return component
        return None


if __name__ == '__main__':
    from webq.base.components.tags_q import div_q as div

    el = div(
        div(
            div(class_="c", data_smth="i like searching"),
            id="b"
        ),
        id="a"
    )
    print(list(HTMLSearcher(el).find_all("div:has(> [data-smth ^= i like])")))
