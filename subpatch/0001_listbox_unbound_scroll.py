from patch import BaseSubPatch


class SubPatch(BaseSubPatch):
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "Do not scroll unbound listboxes to the end (listbox.cpp)"
        self.target_file = "bootable/recovery/gui/listbox.cpp"

        # A listbox with no variable has an empty mVariable, and a general refresh
        # passes an empty varName, so every item's empty variableValue matches and
        # the list lands on its last item (Advanced opens scrolled partway down).
        self.CHANGES = [
            (
                r"""		else if (varName == mVariable) {
			if (item.variableValue == currentValue) {""",
                r"""		else if (varName == mVariable && !mVariable.empty()) {
			if (item.variableValue == currentValue) {""",
            ),
        ]
