from asgiref.sync import sync_to_async


class EnergyScraperPipeline:
    async def process_item(self, item, spider):
        await self.save_item_sync(item)
        return item

    @sync_to_async
    def save_item_sync(self, item):
        item.save()
