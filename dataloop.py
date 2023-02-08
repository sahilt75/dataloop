import dtlpy as dl
import time


class DataLoop:
    def __init__(self):
        # a. Create a new dataset (if existing, get it)
        project = dl.projects.get(project_name='demo-project')
        self.dataset = project.datasets.get(dataset_name='Cars')

    def login(self):
        dl.login_m2m(email="bot.175aa789-39e0-4365-bd44-e86720ad736d@bot.dataloop.ai", password="92h#0@!5Tb65izfG9")

    def annotate_item(self,item_id,labels=[],attributes=[],type="classification",template_id=None):
        """
        Applies classification label to item
        :param item: item id
        :param label: label
        :return:
        """
        item_obj = self.dataset.items.get(item_id=item_id)
        builder = item_obj.annotations.builder()
        for label in labels:
            if type == "classification":
                builder.add(annotation_definition=dl.Classification(label=label,attributes=attributes))
            else:
                builder.add(annotation_definition=dl.Pose(label=label, template_id=template_id))
        item_obj.annotations.upload(builder)


    def dataloop_functions(self):

        # b. Add three labels to the dataset recipe (class1, class2, and key)
        self.dataset.add_labels([
            {"label_name":'class1'},
            {"label_name":'class2'},
            {"label_name":'key'},
        ])

        # c. upload directory with five images (Single upload to all items in the
        # directory)
        # d. Add a UTM metadata to an item user metadata - collection time
        # Note: Have made an assumption here that UTM would be UTC here
        self.dataset.items.upload(local_path="./racing-cars/", remote_path="/sdk-uploads/", item_metadata={"collected":time.time()})

        # e. Add a classification of class1 to the first two of the images you uploaded.
        # f. Add a classification of class2 to the rest of the images you uploaded.
        self.annotate_item("63dfa1a0ed3655175f3d7759",["class1"])
        self.annotate_item("63dfa1a047a4833d7ea97d99",["class1"])
        self.annotate_item("63dfa1a041307c86319bd45a",["class2"])
        self.annotate_item("63dfa1a01632906c1a121d62",["class2"])
        self.annotate_item("63dfa1a00bb943021549e2f5",["class2"])

        # g. Add five random key points with the label “key” to one item.
        recipe = self.dataset.recipes.get(recipe_id='63df83d5a2836593c9b839e2')
        template_id = recipe.get_annotation_template_id(template_name="Key Annotation")
        self.annotate_item("63e3c69774e98c27f876df54",["key"],type="pose",template_id=template_id)

    def filter_data(self):
        # Create a query that selects only image items that have been labeled as class1
        # and print the item name and item id of each item
        filters = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
        filters.add(field='label', values='class1')
        pages = self.dataset.annotations.list(filters=filters)
        for page in pages:
            for item in page:
                item.print()

        # Create a query that retrieves all point annotations from the dataset and prints the
        # item name and item id of each item, and for each item, print for each annotation
        # the annotation id, annotation label, and position of the point (x,y)
        filters = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
        filters.add(field='type', values='point')
        pages = self.dataset.annotations.list(filters=filters)
        for page in pages:
            for annotation in page:
                annotation.print()


if __name__ == "__main__":
    dataloop_obj = DataLoop()

    # Login for dataloop platform
    dataloop_obj.login()

    # Dataloop functions
    dataloop_obj.dataloop_functions()

    # Filter queries
    dataloop_obj.filter_data()