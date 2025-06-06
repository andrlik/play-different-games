# models.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.db import models
from django.utils.translation import gettext_lazy as _
from isbn_field.fields import ISBNField

from play_different_games.core.models import SluggedUUIDTimestampedModel

# Create your models here.


class SourceBookTypeChoices(models.TextChoices):
    """
    Type choices for Sourcebooks.
    """

    COREBOOK = "core", _("Corebook")
    BESTIARY = "bestiary", _("Bestiary")
    GM_GUIDE = "gm_guide", _("GM Guide")
    ADVENTURE = "adventure", _("Adventure or Campaign")
    SETTING = "setting", _("Setting guide")
    FICTION = "fiction", _("Tie-in Fiction")
    EXPANDED = "expanded", _("Expanded rules for game.")


class CardSets(models.TextChoices):
    """
    Card set choice list.
    """

    STANDARD_DECK = (
        "s52",
        _("52 Standard Playing Cards - Jokers removed"),
    )
    JOKER_DECK = "sjk", _("Standard Playing Cards with Jokers included")
    TAROT_DECK = "tarot", _("Tarot Deck")
    CUSTOM_DECK = "cust", _("Custom set of cards for game.")
    CUSTOM_DECK_OPT = (
        "copt",
        _("Custom deck of cards for game with option to substitute standard cards."),
    )


class DiceSets(models.TextChoices):
    """
    Dice sets for use in game mechanics.
    """

    POLYHEDRAL_ARRAY = "poly", _("Standard array: d20, d10, d100, d12, d8, d6, d4")
    D4 = "d4", _("D4s only.")
    D6X2 = "2d6", _("2d6")
    D6 = "d6", _("D6s only.")
    D8 = "d8", _("D8s only.")
    D10 = "d10", _("D10s only.")
    D12 = "d12", _("D12s only.")
    D20 = "d20", _("D20s only.")
    D100 = "d100", _("D100s only.")
    CYPHER_SET = "cypher", _("Cypher array: d20, d100, d6")
    FATE = "fate", _("Fate or Fudge Dice")
    GENESYS = "genesys", _("Genesys Narrative Dice")


class ProductTypeChoices(models.TextChoices):
    """
    Product type choices for models.
    """

    SOURCEBOOK = "book", _("Source Book")
    ACCESSORY = "accessory", _("Accessory")
    GAMEBOX = "box", _("Game Box")


class GameLicense(SluggedUUIDTimestampedModel):
    """
    Defines a given game license that may be applied to a work.

    Attributes:
        id (uuid): UUID4 primary key.
        title (str): Title of license (include version in title)
        slug (str): Unique slug for license.
        created (datetime): Creation time of record.
        modified (datetime): Time of last modification.
        description (str | None): Description of license.
        creative_commons (bool): Is this a creative commons license.
        ogl_compatible (bool): Compatible with OGL 1.0?
        viral (bool): Requires works released under same license?
        allows_commercial_adaptations (bool): Allows commercial use?
        requires_royalty (bool): Is royalty payment and sales reporting required?
        url (str | None): URL where more info can be found.
    """

    title = models.CharField(
        max_length=250, help_text=_("Title of license including version number.")
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=_("Brief summary of the license is but not the full legal text."),
    )
    creative_commons = models.BooleanField(
        default=False,
        help_text=_("Is this license a Creative Commons or compatible license?"),
    )
    ogl_compatible = models.BooleanField(
        default=False, help_text=_("Is this compatible with OGL 1.0 licenses?")
    )
    viral = models.BooleanField(
        default=False,
        help_text=_(
            "Does this require derivitive works to release all their content under the "
            "same license?"
        ),
    )
    allows_commercial_adaptations = models.BooleanField(
        default=False,
        help_text=_(
            "Can you make commercial works off of this license without a separate "
            "licensing agreement?"
        ),
    )
    requires_royalty = models.BooleanField(
        default=False,
        help_text=_("Does this require a royalty from the sales of derivative works?"),
    )

    url = models.URLField(
        null=True,
        blank=True,
        help_text=_("URL where more info on the license may be found, if any."),
    )

    def __str__(self):
        return self.title  # no cov

    class Meta:
        ordering = ["title"]

    class SlugMeta:
        slug_based_on_fields = ["title"]


class Publisher(SluggedUUIDTimestampedModel):
    """
    A game publication company.

    Attributes:
        id (uuid): UUID4 primary key.
        name (str): Name of publisher.
        slug (str): Unique slug for publisher.
        created (datetime): Creation time of record.
        modified (datetime): Time of last modification.
        founded_on (date | None): Date founded.
        closed_on (date | None): Date closed.
        url (str | None): URL for company, if any.
        description (str | None): Description of company.
        logo (ImageFile | None): Company logo
    """

    name = models.CharField(max_length=250, help_text=_("Name of publishing company."))
    founded_on = models.DateField(
        null=True, blank=True, help_text=_("What date was company founded?")
    )
    closed_on = models.DateField(
        null=True, blank=True, help_text=_("When company closed.")
    )
    url = models.URLField(null=True, blank=True, help_text=_("Company URL"))
    description = models.TextField(
        null=True, blank=True, help_text=_("Short description of the company.")
    )
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to="catalog/publisher_logos/%Y/%m/%d",
        help_text=_("Publisher logo"),
    )

    def __str__(self):  # no cov
        return self.name

    class Meta:
        ordering = ["name", "-founded_on"]

    class SlugMeta:
        slug_based_on_fields = ["name"]


class Author(SluggedUUIDTimestampedModel):
    """
    Author or designer for a game.

    Attributes:
        id (uuid): UUID4 primary key.
        last_name (str): Surname of author.
        first_name (str): Given name of author.
        display_name (str | None): Display name of author if not related to other names.
        deadname (bool): If this name shouldn't be considered their name anymore.
        slug (str): Unique slug for publisher.
        created (datetime): Creation time of record.
        modified (datetime): Time of last modification.
    """

    last_name = models.CharField(
        _("Surname"), max_length=100, help_text=_("Surname of author.")
    )
    first_name = models.CharField(
        _("Given name"), max_length=100, help_text=_("Given name of author.")
    )
    display_name = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Display name of author if different from their name of record."),
    )
    deadname = models.BooleanField(
        default=False,
        help_text=_(
            "Should this be considered a deadname and not the preferred search "
            "approach for finding records?"
        ),
    )

    def __str__(self):
        """
        Use display_name if present, otherwise concatenate first and last name.
        """
        if self.display_name:
            return self.display_name
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["display_name", "last_name", "first_name"]

    class SlugMeta:
        slug_based_on_fields = ["first_name", "last_name"]


class GameSystem(SluggedUUIDTimestampedModel):
    """
    Model for a given game system.

    Attributes:
        id (uuid): Primary key of record.
        title (str): Title of game system.
        slug (str): Slug for game system.
        release_date (date | None): Release date for the system.
        description (str | None): Description of the system.
        srd (bool): Is this system avaialble as an SRD?
        srd_release_date (date | None): Release date of the SRD, if any.
        open_licensing (bool): Does this system have some sort of open license?
        publisher (Publisher): Publishing company behind this system.
        licenses (GameLicense): Many to Many list of GameLicenses avaialble for system.
        primary_resolution_mechanic (str): Primary test method.
        secondary_resolution_mechanic (str | None): Secondary test method, if any.
        url (str | None): URL for system, if any.
        primary_authors (Author): Many to many relation with primary authors.
        additional_authors (Author): Many to many relation with additional contributors.
        cards_used (str | None): Card types used in game.
        dice_used (str | None): Dice types used in game.
        exploding_dice (bool): Does it use an exploding dice mechanic?
        playbooks (bool): Does the system use playbooks?
        minis_required (bool): Does the game require minis/battlemaps to play?
        tokens (bool): Does this have a metacurrency in play?
        partial_success (bool): Does this have a partial success mechanic?
        gm_less (bool): Is this game intended to be played without a GM?
        solo (bool): Is this a game designed for solo play?
        img (ImageFile | None): Display image for system.
        created (datetime): When this record was created.
        modified (datetime): When this record was last updated.
    """

    class MechanicChoices(models.TextChoices):
        """
        Text choices for Mechanic types.
        """

        DICE = "dice", _("Dice")
        CARD = "card", _("Cards")
        CUSTOM = "custom", _("Other custom mechanic")

    title = models.CharField(
        max_length=300,
        unique=True,
        help_text=_("Title of game system including version."),
    )
    release_date = models.DateField(
        null=True, blank=True, help_text=_("Initial release for this game system.")
    )
    description = models.TextField(
        null=True, blank=True, help_text=_("Description of the system.")
    )
    srd = models.BooleanField(
        default=False, help_text=_("Is system available as a separate SRD?")
    )
    srd_release_date = models.DateField(
        null=True,
        blank=True,
        help_text=_(
            "Release date of the SRD, which may be after initial game release."
        ),
    )
    open_licensing = models.BooleanField(
        default=False, help_text=_("Supports an open licensing scheme of some type.")
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Publisher of the game system?"),
    )
    licenses = models.ManyToManyField(
        GameLicense, help_text=_("Allowed licenses for use."), blank=True
    )
    primary_resolution_mechanic = models.CharField(
        max_length=20,
        choices=MechanicChoices.choices,
        default=MechanicChoices.DICE,
        help_text=_("Primary method of resolving player actions."),
    )
    secondary_resolution_mechanic = models.CharField(
        max_length=20,
        choices=MechanicChoices.choices,
        null=True,
        blank=True,
        help_text=_("Secondary mechanic, if any."),
    )
    url = models.URLField(
        null=True, blank=True, help_text=_("URL for the system if any.")
    )
    primary_authors = models.ManyToManyField(
        Author,
        related_name="systems_authored",
        help_text=_("Primary author/designers for system."),
        blank=True,
    )
    additional_authors = models.ManyToManyField(
        Author,
        related_name="systems_contributed",
        help_text=_("Secondary author/designers credited."),
        blank=True,
    )
    cards_used = models.CharField(
        max_length=20,
        choices=CardSets,
        null=True,
        blank=True,
        help_text=_("Cards used, if any."),
    )
    dice_used = models.CharField(
        max_length=20,
        choices=DiceSets,
        null=True,
        blank=True,
        help_text=_("Dice sets used, if any."),
    )
    exploding_dice = models.BooleanField(
        default=False, help_text=_("Is there an exploding dice mechanic?")
    )
    playbooks = models.BooleanField(
        default=False, help_text=_("Are playbooks used for character/group sheets.")
    )
    minis_required = models.BooleanField(
        default=False, help_text=_("Does this game require minatures/battle maps?")
    )
    tokens = models.BooleanField(
        default=False,
        help_text=_(
            "Does this system use a meta currency such as Fate points, XP pay, etc?"
        ),
    )
    partial_success = models.BooleanField(
        default=False,
        help_text=_("Does this system implement a partial success/failure mechanic?"),
    )
    gm_less = models.BooleanField(
        default=False, help_text=_("Is this game played without a GM?")
    )
    solo = models.BooleanField(
        default=False, help_text=_("Is this game designed for solo play?")
    )
    img = models.ImageField(
        null=True,
        blank=True,
        upload_to="catalog/game_system_covers/%Y/%m/%d",
        help_text=_("Example image for game system."),
    )

    def __str__(self):  # no cov
        return self.title

    class Meta:
        ordering = ["title"]

    class SlugMeta:
        slug_based_on_fields = ["title"]


class Game(SluggedUUIDTimestampedModel):
    """
    A published game, which may have multiple editions, and each edition may
    use a different system. Different editions may also be released by different
    publishers.

    Attributes:
        id (uuid): Primary key for the record.
        title (str): Title of the game.
        slug (str): Slug for the game.
        created (datetime): When this record was created.
        modified (datetime): When this record was last updated.
        img (ImageFile | None): An image file to display for the game.
        url (str | None): URL for the game, if any.
    """

    title = models.CharField(max_length=200, help_text=_("Title of game"))
    img = models.ImageField(
        null=True,
        blank=True,
        upload_to="catalog/games/%Y/%m/%d",
        help_text=_("Display image for the game."),
    )
    url = models.URLField(
        null=True, blank=True, help_text=_("URL for the game, if any.")
    )

    def __str__(self):  # no cov
        return self.title

    class Meta:
        ordering = ["title"]

    class SlugMeta:
        slug_based_on_fields = ["title"]


class Edition(SluggedUUIDTimestampedModel):
    """
    An individual edition or expansion of a game.

    Attributes:
        id (uuid): Primary key.
        game (Game): Foreign key to Game.
        system (GameSystem): Foreign key to GameSystem.
        edition_identifier (str): Subtitle used to identify this edition.
        slug (str): Slug generated from edition identifier.
        description (str | None): Description of edition.
        release_date (date | None): Initial date of release for edition.
        img (ImageFile | None): Display image for edition.
        url (str | None): URL for edition, if any.
        created (datetime): When this record was created.
        modified (datetime): When this record was last updated.
    """

    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, help_text=_("Game this edition belongs to?")
    )
    system = models.ForeignKey(
        GameSystem,
        on_delete=models.CASCADE,
        help_text=_("Game System used by this edition."),
    )
    edition_identifier = models.CharField(
        max_length=100, help_text=_("Subtitle used to identify this edition.")
    )
    description = models.TextField(
        null=True, blank=True, help_text=_("Description of this edition.")
    )
    release_date = models.DateField(
        null=True, blank=True, help_text="Initial release of this edition."
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        help_text=_("Initial publisher of edition."),
    )
    img = models.ImageField(
        null=True,
        blank=True,
        upload_to="catalog/editions/%Y/%m/%d",
        help_text=_("Display image for this edition."),
    )
    url = models.URLField(
        null=True, blank=True, help_text=_("URL for this edition, if any.")
    )

    def __str__(self):  # no cov
        return f"{self.game.title} {self.edition_identifier}"

    class Meta:
        ordering = ["release_date", "edition_identifier"]

    class SlugMeta:
        slug_based_on_fields = ["edition_identifier"]


class Product(SluggedUUIDTimestampedModel):
    """
    A sourcebook published for a given game edition.

    Attributes:
        id (uuid): Primary key of product.
        edition (Edition): Related game edition.
        title (str): Title of product.
        product_type (str): Type of product.
        sourcebook_type (str | None): Type of sourcebook if applicable.
        isbn (str | None): ISBN, if any.
        release_date (date | None): First printing date, if known.
        primary_authors (Author): Many to many relation with authors.
        additional_authors (Author): Many to many relation with contributors.
        img (ImageFile | None): Display image for product, if any.
        url (str | None): URL for product, if any.
        created (datetime): When this record was created.
        modified (datetime): When this record was last updated.
    """

    edition = models.ForeignKey(
        Edition,
        on_delete=models.CASCADE,
        help_text=_("Which edition this product is associated with."),
    )
    title = models.CharField(max_length=200, help_text=_("Product title"))
    product_type = models.CharField(
        max_length=20,
        choices=ProductTypeChoices,
        default=ProductTypeChoices.SOURCEBOOK,
        help_text=_("What type of product is this?"),
    )
    sourcebook_type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=SourceBookTypeChoices,
        help_text=_("If this is a sourcebook, what type of book is it?"),
    )
    isbn = ISBNField(null=True, blank=True, help_text=_("ISBN of product, if any."))
    release_date = models.DateField(
        null=True, blank=True, help_text=_("First printing of this product.")
    )
    primary_authors = models.ManyToManyField(
        Author,
        blank=True,
        help_text=_("Primary credited authors/designers."),
        related_name="products_authored",
    )
    additional_authors = models.ManyToManyField(
        Author,
        blank=True,
        help_text=_("Additional credited contributors."),
        related_name="products_contributed",
    )
    img = models.ImageField(
        null=True,
        blank=True,
        upload_to="catalog/products/%Y/%m/%d",
        help_text=_("Display image for product."),
    )
    url = models.URLField(
        null=True, blank=True, help_text=_("URL for product, if any.")
    )
    available_print = models.BooleanField(
        default=False, help_text=_("Available in print?")
    )
    available_digital = models.BooleanField(
        default=True, help_text=_("Available in digital?")
    )

    def __str__(self):  # no cov
        return self.title

    class Meta:
        ordering = [
            "edition__game__title",
            "edition__edition_identifier",
            "title",
            "release_date",
        ]

    class SlugMeta:
        slug_based_on_fields = ["title"]
