# Copyright 2014, 2015, Nik Kinkel and David Johnston
# See LICENSE for licensing information

PAYLOAD_START_V3 = 3
PAYLOAD_START_V4 = 5

PAYLOAD_FIELD_LEN = 2

MAX_PAYLOAD_LEN  = 509
MAX_RPAYLOAD_LEN = 498

FIXED_LEN_V3_LEN = 512
FIXED_LEN_V4_LEN = 514

V3_CIRCUIT_LEN = 2
V4_CIRCUIT_LEN = 4

IPv4_ADDR_LEN = 4
IPv6_ADDR_LEN = 16

HOSTNAME_TYPE       = 0x00
IPv4_ADDR_TYPE      = 0x04
IPv6_ADDR_TYPE      = 0x06

# Cell command fields
PADDING_CMD         = 0
CREATE_CMD          = 1
CREATED_CMD         = 2
RELAY_CMD           = 3
DESTROY_CMD         = 4
CREATE_FAST_CMD     = 5
CREATED_FAST_CMD    = 6
VERSIONS_CMD        = 7
NETINFO_CMD         = 8
RELAY_EARLY_CMD     = 9
CREATE2_CMD         = 10
CREATED2_CMD        = 11
VPADDING_CMD        = 128
CERTS_CMD           = 129
AUTH_CHALLENGE_CMD  = 130
AUTHENTICATE_CMD    = 131
AUTHORIZE_CMD       = 132

PADDING_CMD_IDS = (
    PADDING_CMD,
    VPADDING_CMD,
)

# Commands used in fixed-length cells
FIXED_LEN_CMD_IDS = (
    PADDING_CMD,
    CREATE_CMD,
    CREATED_CMD,
    RELAY_CMD,
    DESTROY_CMD,
    CREATE_FAST_CMD,
    CREATED_FAST_CMD,
    NETINFO_CMD,
    RELAY_EARLY_CMD,
    CREATE2_CMD,
    CREATED2_CMD,
)

# Commands used in variable-length cells
VAR_LEN_CMD_IDS = (
    VERSIONS_CMD,
    VPADDING_CMD,
    CERTS_CMD,
    AUTH_CHALLENGE_CMD,
    AUTHENTICATE_CMD,
    AUTHORIZE_CMD,
)

CELL_CMD_IDS = FIXED_LEN_CMD_IDS + VAR_LEN_CMD_IDS

# Relay cell commands
RELAY_BEGIN_CMD     = 1
RELAY_DATA_CMD      = 2
RELAY_END_CMD       = 3
RELAY_CONNECTED_CMD = 4
RELAY_SENDME_CMD    = 5
RELAY_EXTEND_CMD    = 6
RELAY_EXTENDED_CMD  = 7
RELAY_TRUNCATE_CMD  = 8
RELAY_TRUNCATED_CMD = 9
RELAY_DROP_CMD      = 10
RELAY_RESOLVE_CMD   = 11
RELAY_RESOLVED_CMD  = 12
RELAY_BEGIN_DIR_CMD = 13
RELAY_EXTEND2_CMD   = 14
RELAY_EXTENDED2_CMD = 15

RELAY_CELL_CMDS = (
    RELAY_BEGIN_CMD,
    RELAY_DATA_CMD,
    RELAY_END_CMD,
    RELAY_CONNECTED_CMD,
    RELAY_SENDME_CMD,
    RELAY_EXTEND_CMD,
    RELAY_EXTENDED_CMD,
    RELAY_TRUNCATE_CMD,
    RELAY_TRUNCATED_CMD,
    RELAY_DROP_CMD,
    RELAY_RESOLVE_CMD,
    RELAY_RESOLVED_CMD,
    RELAY_BEGIN_DIR_CMD,
    RELAY_EXTEND2_CMD,
    RELAY_EXTENDED2_CMD,
)

# Reasons a RelayEndCell may be sent or received
REASON_MISC             = 1
REASON_RESOLVEFAILED    = 2
REASON_CONNECTREFUSED   = 3
REASON_EXITPOLICY       = 4
REASON_DESTROY          = 5
REASON_DONE             = 6
REASON_TIMEOUT          = 7
REASON_NOROUTE          = 8
REASON_HIBERNATING      = 9
REASON_INTERNAL         = 10
REASON_RESOURCELIMIT    = 11
REASON_CONNRESET        = 12
REASON_TORPROTOCOL      = 13
REASON_NOTDIRECTORY     = 14

# Reasons a DestroyCell or a RelayTruncatedCell may be sent or received
DESTROY_NONE              = 0
DESTROY_PROTOCOL          = 1
DESTROY_INTERNAL          = 2
DESTROY_REQUESTED         = 3
DESTROY_HIBERNATING       = 4
DESTROY_RESOURCELIMIT     = 5
DESTROY_CONNECTFAILED     = 6
DESTROY_OR_IDENTITY       = 7
DESTROY_OR_CONN_CLOSED    = 8
DESTROY_FINISHED          = 9
DESTROY_TIMEOUT           = 10
DESTROY_DESTROYED         = 11
DESTROY_NOSUCHSERVICE     = 12

DESTROY_TRUNCATE_REASONS = (
    DESTROY_NONE,
    DESTROY_PROTOCOL,
    DESTROY_INTERNAL,
    DESTROY_REQUESTED,
    DESTROY_HIBERNATING,
    DESTROY_RESOURCELIMIT,
    DESTROY_CONNECTFAILED,
    DESTROY_OR_IDENTITY,
    DESTROY_OR_CONN_CLOSED,
    DESTROY_FINISHED,
    DESTROY_TIMEOUT,
    DESTROY_DESTROYED,
    DESTROY_NOSUCHSERVICE,
)

FORWARD_CELLS  = (
    RELAY_BEGIN_CMD,
    RELAY_DATA_CMD,
    RELAY_END_CMD,
    RELAY_SENDME_CMD,
    RELAY_EXTEND_CMD,
    RELAY_TRUNCATE_CMD,
    RELAY_DROP_CMD,
    RELAY_RESOLVE_CMD,
    RELAY_BEGIN_DIR_CMD,
    RELAY_EXTEND2_CMD,
)

BEGIN_FLAG_IPv6_OK          = 1
BEGIN_FLAG_IPv4_NOT_OK      = 2
BEGIN_FLAG_IPv6_PREFERRED   = 3

RELAY_BEGIN_FLAGS = (
    BEGIN_FLAG_IPv6_OK,
    BEGIN_FLAG_IPv4_NOT_OK,
    BEGIN_FLAG_IPv6_PREFERRED,
)

NTOR_HTYPE = 2
NTOR_HLEN  = 84

LSTYPE_IPv4     = 0
LSTYPE_IPv6     = 1
LSTYPE_LEGACY   = 2
LSLEN_IPv4      = 6
LSLEN_IPv6      = 18
LSLEN_LEGACY    = 20

RECOGNIZED      = "\x00\x00"
EMPTY_DIGEST    = "\x00\x00\x00\x00"