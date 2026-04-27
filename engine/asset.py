from enum import IntEnum, auto


class AssetID(IntEnum):
    TEX_TILE_GRASS = auto()
    TEX_ANIM_SLIME = auto()


class Assets:

    def __init__(self):
        self.paths: dict[int, str] = {
            AssetID.TEX_TILE_GRASS: "../art/iso_tile_grass.png",
            AssetID.TEX_ANIM_SLIME: "../art/slime_anim.png",
        }

    def get_path(self, asset_id: AssetID) -> str:
        return self.paths[asset_id.value]
