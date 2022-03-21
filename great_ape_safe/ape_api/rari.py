from brownie import interface
from helpers.addresses import registry


class Rari():
    def __init__(self, safe):
        self.safe = safe

        # contracts
        self.unitroller = interface.IRariComptroller(
            registry.eth.rari.unitroller, owner=self.safe.account
        )


    def ftoken_is_paused(self, ftoken_addr):
        return self.unitroller.borrowGuardianPaused(ftoken_addr)


    def ftoken_pause(self, ftoken_addr):
        ftoken = interface.IFToken(ftoken_addr, owner=self.safe.account)
        self.unitroller._setBorrowPaused(ftoken_addr, True)
        if ftoken.reserveFactorMantissa() != 0:
            ftoken._setReserveFactor(0)
        assert self.ftoken_is_paused(ftoken_addr)
        assert ftoken.reserveFactor() == 0


    def ftoken_unpause(self, ftoken_addr, rf=0.15):
        ftoken = interface.IFToken(ftoken_addr, owner=self.safe.account)
        self.unitroller._setBorrowPaused(ftoken_addr, False)
        if ftoken.reserveFactorMantissa() / 1e18 != rf:
            ftoken._setReserveFactor(rf * 1e18)
        assert self.ftoken_is_paused(ftoken_addr) is False
        assert ftoken.reserveFactorMantissa() / 1e18 == rf


    def ftoken_is_listed(self, ftoken_addr):
        is_listed, _ = self.unitroller.markets(ftoken_addr)
        return is_listed


    def ftoken_get_cf(self, ftoken_addr):
        _, cf_mantissa = self.unitroller.markets(ftoken_addr)
        return cf_mantissa / 1e18


    def ftoken_set_cf(self, ftoken_addr, cf):
        self.unitroller._setCollateralFactor(ftoken_addr, cf * 1e18)
        assert self.ftoken_get_cf(ftoken_addr) == cf


    def ftoken_get_rate_model(self, ftoken_addr):
        ftoken = interface.IFToken(ftoken_addr, owner=self.safe.account)
        return ftoken.interestRateModel()


    def ftoken_set_rate_model(self, ftoken_addr, rate_model_addr):
        ftoken = interface.IFToken(ftoken_addr, owner=self.safe.account)
        ftoken._setInterestRateModel(rate_model_addr)
        assert self.ftoken_get_rate_model(ftoken_addr) == rate_model_addr


    def ftoken_get_admin_fee(self, ftoken_addr):
        ftoken = interface.IFToken(ftoken_addr, owner=self.safe.account)
        return ftoken.adminFeeMantissa() / 1e18


    def ftoken_set_admin_fee(self, ftoken_addr, admin_fee):
        ftoken = interface.IFToken(ftoken_addr, owner=self.safe.account)
        ftoken._setAdminFee(admin_fee * 1e18)
        assert self.ftoken_get_admin_fee(ftoken_addr) == admin_fee


    def add_ftoken_to_pool(self, ftoken_addr, cf=None):
        assert ftoken_addr not in self.unitroller.getAllMarkets()
        if cf:
            self.unitroller._supportMarketAndSetCollateralFactor(ftoken_addr, cf * 1e18)
        else:
            self.unitroller._supportMarket(ftoken_addr)
        assert ftoken_addr in self.unitroller.getAllMarkets()


    def upgrade_comptroller(self, implementation):
        self.unitroller._setPendingImplementation(implementation)
        assert self.unitroller.pendingComptrollerImplementation() == implementation
        comptroller = interface.IRariComptroller(
            implementation, owner=self.safe.account
        )
        comptroller._become(self.unitroller.address)
        assert self.unitroller.comptrollerImplementation() == implementation


    def upgrade_ftoken(self, ftoken_addr, implementation, allow_resign=False):
        ftoken = interface.IFToken(ftoken_addr, owner=self.safe.account)
        ftoken._setImplementation(implementation, allow_resign, b'')
        assert ftoken.implementation() == implementation
