from ACTION_TYPE import ACTION_TYPE
from DPS_Exceptions import ReadException


class Parse_Line(object):

    failed = ['try']

    ATTACK_TYPE = 8
    ORIGINATOR = 6
    DMG = 12

    def parse(self, line, grp_data):
        """parses incoming line.

        Args:
            line: Line to parse"""
        # Parse_Line.validate_line(line)
        if grp_data.in_group(line[Parse_Line.ORIGINATOR]):
            if Parse_Line.is_dps_line(line):
                Parse_Line.parse_dps_line(line, grp_data)

    def is_dps_line(self, line):
        if ACTION_TYPE.melee_attack_word(line[Parse_Line.ATTACK_TYPE]) is not False:
            return True

    def parse_dps_line(self, line, grp_data):
        grp_data.add_damage([Parse_Line.ORIGINATOR],
                            ACTION_TYPE.melee_attack_word(line[Parse_Line.ATTACK_TYPE]),
                            [Parse_Line.DMG])

    def validate_line(self, line):
        if line[Parse_Line.ORIGINATOR] not in Parse_Line.group:
            raise ReadException(line[Parse_Line.ORIGINATOR] + "Not in group")