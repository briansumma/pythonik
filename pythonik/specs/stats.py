from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from pythonik.models.base import Response
from pythonik.models.stats import (
    AssetUsageSchema,
    AssetUsagesSchema,
    AutomationRunsSchema,
    BillingCreditsSchema,
    BillingCreditsVerifySchema,
    BillingCustomerCardSchema,
    BillingCustomerSchema,
    BillingExpirationUpdateSchema,
    BillingReceiptSchema,
    BillingRecipientsSchema,
    BillingSchema,
    BillingSettingsSchema,
    BillingsSchema,
    BillingStatsSchema,
    CollectionUsageSchema,
    CreditsSchema,
    CurrentUsageSchema,
    LogsRecipientReadSchema,
    LogsRecipientSchema,
    LogsRecipientsSchema,
    PriceSchema,
    PricesSchema,
    StorageAccessesSchema,
    StorageUsagesSchema,
    TranscoderUsagesSchema,
    UserUsagesSchema,
)
from pythonik.specs._internal_utils import is_pydantic_model
from pythonik.specs.base import Spec


class StatsSpec(Spec):
    server = "API/stats/"

    def create_asset_usage(
        self,
        asset_usage: Union[AssetUsageSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Sets asset usage.

        Args:
            asset_usage: Asset usage data (either as AssetUsageSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AssetUsageSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (asset_usage.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(asset_usage) else asset_usage)
        url = self.gen_url("assets/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, AssetUsageSchema)

    def list_asset_usage_by_period(
        self,
        period: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns all asset usage.

        Required roles:
            - can_read_stats

        Args:
            period: Period of stats (month or day)
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AssetUsagesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        url = self.gen_url(f"assets/by/{period}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, AssetUsagesSchema)

    def list_automation_runs_by_day(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns automation runs by day.

        Required roles:
            - can_read_stats

        Args:
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationRunsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        url = self.gen_url("automations/usage/by/day/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, AutomationRunsSchema)

    def list_billing(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        per_page: int = 100,
        last_id: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns billing info.

        Required roles:
            - can_read_stats

        Args:
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            per_page: The number of items for each page (default: 100)
            last_id: ID of a last file on previous page (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params: Dict[str, Any] = {"per_page": per_page}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if last_id:
            params["last_id"] = last_id

        url = self.gen_url("billing/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, BillingsSchema)

    def create_billing(
        self,
        billing: Union[BillingSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Updates Billing (Requires super admin access).

        Args:
            billing: Billing data (either as BillingSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (billing.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(billing) else billing)
        url = self.gen_url("billing/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, BillingSchema)

    def get_billing_receipt(
        self,
        charge_id: str,
        **kwargs,
    ) -> Response:
        """
        Returns billing receipt.

        Required roles:
            - can_read_billing

        Args:
            charge_id: ID of the charge
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingReceiptSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"billing/charges/{charge_id}/receipt_url/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, BillingReceiptSchema)

    def create_billing_credits(
        self,
        credit_amount: Union[BillingCreditsSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Add credits to an account.

        Required roles:
            - can_write_billing

        Args:
            credit_amount: Credits data (either as BillingCreditsSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingCreditsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (credit_amount.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(credit_amount) else credit_amount)
        url = self.gen_url("billing/credits/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, BillingCreditsSchema)

    def get_credits_price(
        self,
        credit_amount: int,
        **kwargs,
    ) -> Response:
        """
        Checks the total price that needs to be paid including VAT if it's
        needed.

        Required roles:
            - can_write_billing

        Args:
            credit_amount: Number of credits to check price for
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=CreditsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {"credits": credit_amount}
        url = self.gen_url("billing/credits/price/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, CreditsSchema)

    def verify_billing_credits(
        self,
        verify_data: Union[BillingCreditsVerifySchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Verify status of add credits to an account.

        Required roles:
            - can_write_billing

        Args:
            verify_data: Verification data (either as BillingCreditsVerifySchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingCreditsVerifySchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (verify_data.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(verify_data) else verify_data)
        url = self.gen_url("billing/credits/verify/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, BillingCreditsVerifySchema)

    def get_billing_customer(
        self,
        **kwargs,
    ) -> Response:
        """
        Returns billing customer.

        Required roles:
            - can_read_billing

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url("billing/customer/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, BillingSchema)

    def update_billing_customer(
        self,
        customer: Union[BillingCustomerSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Updates billing customer.

        Required roles:
            - can_write_billing

        Args:
            customer: Customer data (either as BillingCustomerSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingCustomerSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (customer.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(customer) else customer)
        url = self.gen_url("billing/customer/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, BillingCustomerSchema)

    def create_billing_customer_card(
        self,
        card: Union[BillingCustomerCardSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Creates billing customer card.

        Required roles:
            - can_write_billing

        Args:
            card: Card data (either as BillingCustomerCardSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingCustomerCardSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (card.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(card) else card)
        url = self.gen_url("billing/customer/card/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, BillingCustomerCardSchema)

    def delete_billing_customer_card(
        self,
        **kwargs,
    ) -> Response:
        """
        Deletes billing customer card.

        Required roles:
            - can_write_billing

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url("billing/customer/card/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def list_billing_invoices(
        self,
        starting_after: Optional[str] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Response:
        """
        Returns billing invoices.

        Required roles:
            - can_read_billing

        Args:
            starting_after: Starting point for the invoice list (optional)
            limit: Limit the number of invoices returned (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        params = {}
        if starting_after:
            params["starting_after"] = starting_after
        if limit:
            params["limit"] = limit

        url = self.gen_url("billing/invoices/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, None)

    def list_price_lists(
        self,
        **kwargs,
    ) -> Response:
        """
        Get All Price Lists.

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=PricesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url("billing/price_lists/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, PricesSchema)

    def update_price_list(
        self,
        price_list: Union[PriceSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Creates or updates a Price List.

        Args:
            price_list: Price list data (either as PriceSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=PriceSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (price_list.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(price_list) else price_list)
        url = self.gen_url("billing/price_lists/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, PriceSchema)

    def get_price_list(
        self,
        name: str,
        currency: str,
        **kwargs,
    ) -> Response:
        """
        Get a Price List.

        Args:
            name: Name of the price list
            currency: Currency of the price list
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=PriceSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url(f"billing/price_lists/{name}/{currency}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, PriceSchema)

    def delete_price_list(
        self,
        name: str,
        currency: str,
        **kwargs,
    ) -> Response:
        """
        Delete a Price list.

        Args:
            name: Name of the price list
            currency: Currency of the price list
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url(f"billing/price_lists/{name}/{currency}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def get_billing_recipients(
        self,
        **kwargs,
    ) -> Response:
        """
        Returns billing recipients.

        Required roles:
            - can_read_billing

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingRecipientsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url("billing/recipients/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, BillingRecipientsSchema)

    def update_billing_recipients(
        self,
        recipients: Union[BillingRecipientsSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Updates Billing Recipients.

        Required roles:
            - can_write_billing

        Args:
            recipients: Recipients data (either as BillingRecipientsSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingRecipientsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (recipients.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(recipients) else recipients)
        url = self.gen_url("billing/recipients/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, BillingRecipientsSchema)

    def get_billing_settings(
        self,
        **kwargs,
    ) -> Response:
        """
        Returns billing settings.

        Required roles:
            - can_read_billing

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingSettingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url("billing/settings/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, BillingSettingsSchema)

    def update_billing_settings(
        self,
        settings: Union[BillingSettingsSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Updates Billing Settings.

        Required roles:
            - can_write_billing

        Args:
            settings: Settings data (either as BillingSettingsSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingSettingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url("billing/settings/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, BillingSettingsSchema)

    def get_billing_status(
        self,
        **kwargs,
    ) -> Response:
        """
        Returns billing status.

        Required roles:
            - can_read_billing

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingStatsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url("billing/status/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, BillingStatsSchema)

    def delete_billing(
        self,
        system_domain_id: str,
        billing_id: str,
        **kwargs,
    ) -> Response:
        """
        Delete billing record (Requires super admin access).

        Args:
            system_domain_id: ID of the system domain
            billing_id: ID of the billing record
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url(f"billing/{system_domain_id}/{billing_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def list_billing_expiration(
        self,
        per_page: int = 100,
        **kwargs,
    ) -> Response:
        """
        Returns billing expiration info.

        Args:
            per_page: The number of items for each page (default: 100)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {"per_page": per_page}
        url = self.gen_url("billing_expiration/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, BillingsSchema)

    def update_billing_expiration(
        self,
        system_domain_id: str,
        billing_id: str,
        expiration_data: Union[BillingExpirationUpdateSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update billing expiration record (Requires super admin access).

        Args:
            system_domain_id: ID of the system domain
            billing_id: ID of the billing record
            expiration_data: Expiration data (either as
                BillingExpirationUpdateSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        body = (expiration_data.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(expiration_data) else expiration_data)
        url = self.gen_url(
            f"billing_expiration/{system_domain_id}/{billing_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, BillingSchema)

    def delete_billing_expiration(
        self,
        system_domain_id: str,
        billing_id: str,
        **kwargs,
    ) -> Response:
        """
        Delete billing expiration record (Requires super admin access).

        Args:
            system_domain_id: ID of the system domain
            billing_id: ID of the billing record
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url(
            f"billing_expiration/{system_domain_id}/{billing_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def list_collection_usage_by_period(
        self,
        period: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns all collection usage.

        Required roles:
            - can_read_stats

        Args:
            period: Period of stats (month or day)
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=CollectionUsageSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        url = self.gen_url(f"collections/by/{period}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, CollectionUsageSchema)

    def get_current_usage(
        self,
        per_page: int = 100,
        **kwargs,
    ) -> Response:
        """
        Returns current usage for PRO/ENTERPRISE system domains.

        Args:
            per_page: The number of items for each page (default: 100)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=CurrentUsageSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {"per_page": per_page}
        url = self.gen_url("current_usage/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, CurrentUsageSchema)

    def get_object_info(
        self,
        object_id: str,
        **kwargs,
    ) -> Response:
        """
        Internal endpoint to convert ID to system domain.

        Args:
            object_id: Object ID
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url(f"id/{object_id}/info/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, None)

    def list_ordway_billing(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        per_page: Optional[int] = None,
        page: int = 1,
        **kwargs,
    ) -> Response:
        """
        Returns billing info.

        Required roles:
            - can_read_stats

        Args:
            from_date: Filter by from_date (optional)
            to_date: Filter by from_date (optional)
            per_page: The number of items for each page (optional)
            page: Which page number to fetch (default: 1)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params: Dict[str, Any] = {"page": page}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if per_page:
            params["per_page"] = per_page

        url = self.gen_url("ordway/billing/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, BillingsSchema)

    def get_ordway_billing_customer(
        self,
        **kwargs,
    ) -> Response:
        """
        Returns billing customer.

        Required roles:
            - can_read_billing

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=BillingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url("ordway/billing/customer/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, BillingSchema)

    def list_ordway_billing_invoices(
        self,
        per_page: Optional[int] = None,
        page: int = 1,
        **kwargs,
    ) -> Response:
        """
        Returns billing invoices.

        Required roles:
            - can_read_billing

        Args:
            per_page: The number of items for each page (optional)
            page: Which page number to fetch (default: 1)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        params = {"page": page}
        if per_page:
            params["per_page"] = per_page

        url = self.gen_url("ordway/billing/invoices/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, None)

    def list_storage_access_by_period(
        self,
        period: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns storage_access for all storages.

        Required roles:
            - can_read_stats

        Args:
            period: Period of stats (month or day)
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=StorageAccessesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        url = self.gen_url(f"storage/access/by/{period}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, StorageAccessesSchema)

    def list_storage_usage_by_period(
        self,
        period: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns storage_usage for all storages.

        Required roles:
            - can_read_stats

        Args:
            period: Period of stats (month or day)
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=StorageUsagesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        url = self.gen_url(f"storage/usage/by/{period}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, StorageUsagesSchema)

    def list_logs_recipients(
        self,
        per_page: int = 10,
        last_id: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Get logs recipients settings.

        Required roles:
            - can_read_logs_recipients

        Args:
            per_page: The number of items for each page (default: 10)
            last_id: ID of a last service account set on previous page
                (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=LogsRecipientsSchema)

        Raises:
            - 401 Token is invalid
            - 404 Logs recipients settings don't exist
        """
        params: Dict[str, Any] = {"per_page": per_page}
        if last_id:
            params["last_id"] = last_id

        url = self.gen_url("system/logs/recipients/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, LogsRecipientsSchema)

    def create_logs_recipient(
        self,
        recipient: Union[LogsRecipientSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create logs recipient settings.

        Required roles:
            - can_write_logs_recipients

        Args:
            recipient: Recipient data (either as LogsRecipientSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=LogsRecipientReadSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (recipient.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(recipient) else recipient)
        url = self.gen_url("system/logs/recipients/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, LogsRecipientReadSchema)

    def get_logs_recipient(
        self,
        logs_recipient_id: str,
        **kwargs,
    ) -> Response:
        """
        Get settings of a logs recipient.

        Required roles:
            - can_read_logs_recipients

        Args:
            logs_recipient_id: ID of the logs recipient
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=LogsRecipientReadSchema)

        Raises:
            - 401 Token is invalid
            - 404 Logs recipients settings don't exist
        """
        url = self.gen_url(f"system/logs/recipients/{logs_recipient_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, LogsRecipientReadSchema)

    def update_logs_recipient(
        self,
        logs_recipient_id: str,
        recipient: Union[LogsRecipientSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change logs recipient settings.

        Required roles:
            - can_write_logs_recipients

        Args:
            logs_recipient_id: ID of the logs recipient
            recipient: Recipient data (either as LogsRecipientSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=LogsRecipientReadSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Logs recipient doesn't exist
        """
        body = (recipient.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(recipient) else recipient)
        url = self.gen_url(f"system/logs/recipients/{logs_recipient_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, LogsRecipientReadSchema)

    def partial_update_logs_recipient(
        self,
        logs_recipient_id: str,
        recipient: Union[LogsRecipientSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change logs recipient settings partially.

        Required roles:
            - can_write_logs_recipients

        Args:
            logs_recipient_id: ID of the logs recipient
            recipient: Recipient data (either as LogsRecipientSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=LogsRecipientReadSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Logs recipient doesn't exist
        """
        body = (recipient.model_dump(exclude_defaults=exclude_defaults,
                                     exclude_unset=True)
                if is_pydantic_model(recipient) else recipient)
        url = self.gen_url(f"system/logs/recipients/{logs_recipient_id}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, LogsRecipientReadSchema)

    def delete_logs_recipient(
        self,
        logs_recipient_id: str,
        **kwargs,
    ) -> Response:
        """
        Delete logs recipient settings.

        Required roles:
            - can_delete_logs_recipients

        Args:
            logs_recipient_id: ID of the logs recipient
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Logs recipient doesn't exist
        """
        url = self.gen_url(f"system/logs/recipients/{logs_recipient_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def test_logs_recipient_connection(
        self,
        logs_recipient_id: str,
        **kwargs,
    ) -> Response:
        """
        Test logs recipient connection.

        Required roles:
            - can_write_logs_recipients

        Args:
            logs_recipient_id: ID of the logs recipient
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Logs recipient doesn't exist
        """
        url = self.gen_url(f"system/logs/recipients/{logs_recipient_id}/")
        resp = self._post(url, **kwargs)
        return self.parse_response(resp, None)

    def list_transcoder_usage_by_period(
        self,
        period: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns transcoder_usage for all transcoders.

        Required roles:
            - can_read_stats

        Args:
            period: Period of stats (month or day)
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=TranscoderUsagesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        url = self.gen_url(f"transcoder/usage/by/{period}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, TranscoderUsagesSchema)

    def list_user_audit_by_period(
        self,
        period: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        system_domain_id: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns all audit.

        Required roles:
            - can_read_stats

        Args:
            period: Period of stats (month, day or day_detailed)
            from_date: Filter by from_date (optional)
            to_date: Filter by to_date (optional)
            system_domain_id: Filter by system_domain_id (Only for super
                admins) (optional)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserUsagesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if system_domain_id:
            params["system_domain_id"] = system_domain_id

        url = self.gen_url(f"user/audit/by/{period}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, UserUsagesSchema)
