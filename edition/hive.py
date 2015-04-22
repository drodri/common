from biicode.common.model.brl.block_cell_name import BlockCellName
from biicode.common.utils.serializer import Serializer, SetDeserializer
from biicode.common.exception import BiiSerializationException
from biicode.common.settings.settings import Settings


class Hive(object):

    def __init__(self):
        self.settings = None
        self._cells = set()  # of BlockCellName

    def update(self, processor_changes):
        """ changes with keys BlockCellnames
        """
        if not processor_changes:
            return
        for name in processor_changes.upserted:
            self._cells.add(name)
        for deleted in processor_changes.deleted:
            self._cells.discard(deleted)

    @property
    def blocks(self):
        return {name.block_name for name in self._cells}

    @property
    def cells(self):
        return self._cells

    SERIAL_CELLS_KEY = 'r'
    SERIAL_SETTINGS = 'd'

    def serialize(self):
        return Serializer().build(
            (Hive.SERIAL_CELLS_KEY, self._cells),
            (Hive.SERIAL_SETTINGS, self.settings)
        )

    @staticmethod
    def deserialize(data):
        try:
            hive = Hive()
            hive._cells = SetDeserializer(BlockCellName).deserialize(data[Hive.SERIAL_CELLS_KEY])
            hive.settings = Settings.deserialize(data[Hive.SERIAL_SETTINGS])
            return hive

        except Exception as e:
            raise BiiSerializationException(e)
