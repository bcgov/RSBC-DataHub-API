import { irpFormJsonInfoType } from '@/types/Forms/IRP';
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({
  namespaced: true
})
class IRP extends VuexModule {

    public irpFormsJson: irpFormJsonInfoType[] = [];
    public irpInfo = {} as irpFormJsonInfoType;  
    
      
    @Mutation
    public setIRPFormsJson(irpFormsJson: irpFormJsonInfoType[]): void {   
        this.irpFormsJson = irpFormsJson;
    }    
    @Action
    public UpdateIRPFormsJson(newIRPFormsJson: irpFormJsonInfoType[]): void {
        this.context.commit('setIRPFormsJson', newIRPFormsJson);
    }
  
    @Mutation
    public setIRPInfo(irpInfo: irpFormJsonInfoType): void {   
        this.irpInfo = irpInfo;        
    }    
    @Action
    public UpdateIRPInfo(newIRPInfo: irpFormJsonInfoType): void {
        this.context.commit('setIRPInfo', newIRPInfo);        
    } 
    
}

export default IRP