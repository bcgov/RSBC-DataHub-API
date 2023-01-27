import { viFormJsonInfoType } from '@/types/Forms/VI';
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({
  namespaced: true
})
class VI extends VuexModule {

    public viFormsJson: viFormJsonInfoType[] = [];
    public viInfo = {} as viFormJsonInfoType;      
      
    @Mutation
    public setVIFormsJson(viFormsJson: viFormJsonInfoType[]): void {   
        this.viFormsJson = viFormsJson;
    }    
    @Action
    public UpdateVIFormsJson(newVIFormsJson: viFormJsonInfoType[]): void {
        this.context.commit('setVIFormsJson', newVIFormsJson);
    }
  
    @Mutation
    public setVIInfo(viInfo: viFormJsonInfoType): void {   
        this.viInfo = viInfo;        
    }    
    @Action
    public UpdateVIInfo(newVIInfo: viFormJsonInfoType): void {
        this.context.commit('setVIInfo', newVIInfo);        
    } 
    
}

export default VI