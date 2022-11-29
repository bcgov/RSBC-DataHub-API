
import { adminUserInfoType, cityInfoType, configurationInfoType, countryInfoType, currentlyEditingFormObjectInfoType, formsInfoType, impoundLotOperatorsInfoType, jurisdictionInfoType, loadedInfoType, pickupLocationInfoType, provinceInfoType, userInfoType, userRoleInfoType, vehicleColourInfoType, vehicleInfoType, vehicleStyleInfoType } from '@/types/Common';
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import vehicleColours from '@/utils/vehicleColours.json';

@Module({
  namespaced: true
})
class Common extends VuexModule {

    public version = "0.7.13";
    public formNames = ["12Hour", "24Hour", "IV", "IRP"];
    
    public agencies: string[] = [];
    public dbReady = false;
    public adminUsers: adminUserInfoType[] = [];
    public cities: cityInfoType[] = [];
    public countries: countryInfoType[] = [];
    public configuration = {environment:"prod"} as configurationInfoType;
    public currently_editing_form_object = {"form_type": null, "form_id": null} as currentlyEditingFormObjectInfoType;
    public formsInfo = {} as formsInfoType;
    public vehicleColours: vehicleColourInfoType[] = vehicleColours;
    public icbcVehicleLookup: any[] = [];
    public impound_lot_operators: impoundLotOperatorsInfoType[] = [];
    public isUserAuthorized = null;
    public isOnline = true;
    public jurisdictions: jurisdictionInfoType[] = [];
    public keycloak = {} as any;
    public loaded = {} as loadedInfoType;
    public pickupLocations: pickupLocationInfoType[] = [];
    public provinces: provinceInfoType[] = [];
    public userRoles: userRoleInfoType[] = [];
    public user = {} as userInfoType;
    public vehicles: vehicleInfoType[] = [];
    public vehicle_styles: vehicleStyleInfoType[] = [];    
    public movedToPrintPage = false;


    @Mutation
    public editExistingForm (payload) {
        this.currently_editing_form_object = {"form_id": payload.form_id, "form_type": payload.form_type}
    }
    @Mutation
    public stopEditingCurrentForm() {
        this.currently_editing_form_object = {"form_id": null, "form_type": null}
    }

    @Mutation
    public populateStaticLookupTables(payload) {
        this[payload.type]=payload.data
    }

    @Mutation
    public resourceLoaded(resource) {
        this.loaded[resource]=true
    }

    @Mutation
    public setAgencies(agencies: string[]): void {
        this.agencies = agencies;
    }
    @Action
    public UpdateAgencies(newAgencies: string[]) {
        this.context.commit("setAgencies", newAgencies);
    }
    
    @Mutation
    public setDbReady(dbReady: boolean): void {   
        this.dbReady = dbReady
    }
    @Action
    public UpdateDbReady(newDbReady: boolean): void {
        this.context.commit('setDbReady', newDbReady)
    }   

    @Mutation
    public setAdminUsers(adminUsers: adminUserInfoType[]): void {   
        this.adminUsers = adminUsers
    }
    @Action
    public UpdateAdminUsersInfo(newAdminUsersInfo: adminUserInfoType[]): void {
        this.context.commit('setAdminUsersInfo', newAdminUsersInfo)
    }

    @Mutation
    public setCities(cities: cityInfoType[]): void {   
        this.cities = cities
    }
    @Action
    public UpdateCities(newCities: cityInfoType[]): void {
        this.context.commit('setCities', newCities)
    }

    @Mutation
    public setCountries(countries: countryInfoType[]): void {   
        this.countries = countries
    }
    @Action
    public UpdateCountries(newCountries: countryInfoType[]): void {
        this.context.commit('setCountries', newCountries)
    }

    @Mutation
    public setConfiguration(configuration: configurationInfoType): void {
        this.configuration = configuration;
    }
    @Action
    public UpdateConfiguration(newConfiguration: configurationInfoType) {
        this.context.commit("setConfiguration", newConfiguration);
    }

    @Mutation
    public setCurrentlyEditingFormObject(currentlyEditingFormObject: currentlyEditingFormObjectInfoType): void {
        this.currently_editing_form_object = currentlyEditingFormObject;
    }
    @Action
    public UpdateCurrentlyEditingFormObject(newCurrentlyEditingFormObject: currentlyEditingFormObjectInfoType) {
        this.context.commit("setCurrentlyEditingFormObject", newCurrentlyEditingFormObject);
    }

    @Mutation
    public setFormsInfo(formsInfo: formsInfoType): void {
        this.formsInfo = formsInfo;
    }
    @Action
    public UpdateFormsInfo(newFormsInfo: formsInfoType) {
        this.context.commit("setFormsInfo", newFormsInfo);
    }

    @Mutation
    public setIcbcVehicleLookup(icbcVehicleLookup: any[]): void {   
        this.icbcVehicleLookup = icbcVehicleLookup
    }
    @Action
    public UpdateIcbcVehicleLookup(newIcbcVehicleLookup: any[]): void {
        this.context.commit('setIcbcVehicleLookup', newIcbcVehicleLookup)
    }

    @Mutation
    public setImpoundLotOperators(impoundLotOperators: impoundLotOperatorsInfoType[]): void {   
        this.impound_lot_operators = impoundLotOperators
    }
    @Action
    public UpdateImpoundLotOperators(newImpoundLotOperators: impoundLotOperatorsInfoType[]): void {
        this.context.commit('setImpoundLotOperators', newImpoundLotOperators)
    }

    @Mutation
    public setIsUserAuthorized(isUserAuthorized: boolean): void {   
        this.isUserAuthorized = isUserAuthorized
    }
    @Action
    public UpdateIsUserAuthorized(newIsUserAuthorized: boolean): void {
        this.context.commit('setIsUserAuthorized', newIsUserAuthorized)
    }   

    @Mutation
    public setIsOnline(isOnline: boolean): void {   
        this.isOnline = isOnline
    }
    @Action
    public UpdateIsOnline(newIsOnline: boolean): void {
        this.context.commit('setIsOnline', newIsOnline)
    }  

    @Mutation
    public setJurisdictions(jurisdictions: jurisdictionInfoType[]): void {   
        this.jurisdictions = jurisdictions
    }
    @Action
    public UpdateJurisdictions(newJurisdictions: jurisdictionInfoType[]): void {
        this.context.commit('setJurisdictions', newJurisdictions)
    }

    @Mutation
    public setKeycloak(keycloak: any): void {   
        this.keycloak = keycloak
    }
    @Action
    public UpdateKeycloak(newKeycloak: any): void {
        this.context.commit('setKeycloak', newKeycloak)
    }  

    @Mutation
    public setLoaded(loaded: loadedInfoType): void {   
        this.loaded = loaded
    }
    @Action
    public UpdateLoaded(newLoaded: loadedInfoType): void {
        this.context.commit('setLoaded', newLoaded)
    }  

    @Mutation
    public setPickupLocations(pickupLocations: pickupLocationInfoType[]): void {   
        this.pickupLocations = pickupLocations
    }
    @Action
    public UpdatePickupLocations(newPickupLocations: pickupLocationInfoType[]): void {
        this.context.commit('setPickupLocations', newPickupLocations)
    }

    @Mutation
    public setProvinces(provinces: provinceInfoType[]): void {   
        this.provinces = provinces
    }
    @Action
    public UpdateProvinces(newProvinces: provinceInfoType[]): void {
        this.context.commit('setProvinces', newProvinces)
    }

    @Mutation
    public setUserRole(userRoles: userRoleInfoType[]): void {   
        this.userRoles = userRoles
    }
    @Action
    public UpdateUserRole(newUserRole: userRoleInfoType[]): void {
        this.context.commit('setUserRole', newUserRole)
    }

    @Mutation
    public  setUser(user: userInfoType): void {
        this.user = user;
    }
    @Action
    public UpdateUser(newUser: userInfoType) {
        this.context.commit("setUser", newUser);
    }

    @Mutation
    public setVehicle(vehicles: vehicleInfoType[]): void {   
        this.vehicles = vehicles
    }
    @Action
    public UpdateVehicle(newVehicle: vehicleInfoType[]): void {
        this.context.commit('setVehicle', newVehicle)
    }

    @Mutation
    public setVehicleStyle(vehicleStyles: vehicleStyleInfoType[]): void {   
        this.vehicle_styles = vehicleStyles
    }
    @Action
    public UpdateVehicleStyle(newVehicleStyle: vehicleStyleInfoType[]): void {
        this.context.commit('setVehicleStyle', newVehicleStyle)
    }
    
    @Mutation
    public  setMovedToPrintPage(movedToPrintPage: boolean): void {
        this.movedToPrintPage = movedToPrintPage;
    }
    @Action
    public UpdateMovedToPrintPage(newMovedToPrintPage: boolean) {
        this.context.commit("setMovedToPrintPage", newMovedToPrintPage);
    }    

}

export default Common