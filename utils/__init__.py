from .text_strings_util import make_string_for_output, deleting_photo_from_list, make_promo_string
from .message_utils import make_output_album

from .admin_change_callback import (StorageForDeletingCategory, StorageForChangingContacts,
                                    StorageForAddingPromoProducts, StorageForChangePlaceData, StorageForChangeImageData)
from .files_worker import make_tuples_from_xml
from .xml_parse import parse_xml
from .appending_db_from_1c import updating_db_from_xml
from .compare_utils import compare_tuple_lists
