from ACTION_TYPE import ACTION_TYPE
from DPS_Exceptions import ReadException


class Parse_Line(object):

    failed = ['try']

    ATTACK_TYPE = 6
    ORIGINATOR = 5
    DMG = 10

    def parse(self, line, grp_data):
        """parses incoming line.

        Args:
            line: Line to parse"""
        # Parse_Line.validate_line(line)
        # print(line)
        if grp_data.in_group(line[Parse_Line.ORIGINATOR]):
            if self.is_dps_line(line):
                return self.parse_dps_line(line, grp_data)

    def is_dps_line(self, line):
        if ACTION_TYPE.melee_attack_word(line[Parse_Line.ATTACK_TYPE]) is not False:
            return True

    def parse_dps_line(self, line, grp_data):
        grp_data.add_damage(line[Parse_Line.ORIGINATOR],
                            ACTION_TYPE.melee_attack_word(line[Parse_Line.ATTACK_TYPE]),
                            self.get_dmg(line))
        return True

    def get_dmg(self, line):
        """Finding damage as it can be in various positions in log line"""
        for pos, token in enumerate(line):
            if token == "for":
                if self.found_damage(line[pos:pos + 3]) is True:
                    return line[pos+1]
        raise ReadException("Couldn't find damage on line " + str(line))

    def found_damage(self, tokens):
        """Checking if subset of three tokens refers to dmg"""
        if tokens[0] == "for" and tokens[2] == "points":
            int(tokens[1])  # Should have try catch here
            return True
        return False


    def validate_line(self, line):
        if line[Parse_Line.ORIGINATOR] not in Parse_Line.group:
            raise ReadException(line[Parse_Line.ORIGINATOR] + "Not in group")