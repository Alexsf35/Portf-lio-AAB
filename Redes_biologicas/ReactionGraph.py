import subprocess
import sys
import os
from graphviz import Digraph

from MyGraph import MyGraph


class MetabolicNetwork(MyGraph):
    def __init__(self, reactions):
        """
        Inicializa a rede metabólica. Pode receber:
        - Um dicionário com reações no formato {'cons': [...], 'prod': [...]}
        - Um dicionário com reações no formato 'A + B => C + D' ou 'A + B <=> C + D'
        """
        super().__init__()
        self.reactions = {}

        for reac, val in reactions.items():
            if isinstance(val, dict) and 'cons' in val and 'prod' in val:
                cons = val['cons']
                prod = val['prod']
                self.reactions[reac] = {'cons': cons, 'prod': prod}
            elif isinstance(val, str) and ('=>' in val or '<=>' in val):
                if '<=>' in val:
                    left, right = val.split('<=>')
                    cons = [m.strip() for m in left.split('+')]
                    prod = [m.strip() for m in right.split('+')]
                    self.reactions[reac] = {'cons': cons, 'prod': prod}
                    reverse_reac = reac + '_R'
                    self.reactions[reverse_reac] = {'cons': prod, 'prod': cons}
                else:
                    left, right = val.split('=>')
                    cons = [m.strip() for m in left.split('+')]
                    prod = [m.strip() for m in right.split('+')]
                    self.reactions[reac] = {'cons': cons, 'prod': prod}
            else:
                raise ValueError(f"Formato inválido na reação '{reac}': {val}")

        for reac, val in self.reactions.items():
            self.add_vertex(reac)
            for met in val['cons']:
                self.add_vertex(met)
                self.add_edge(met, reac)
            for met in val['prod']:
                self.add_vertex(met)
                self.add_edge(reac, met)

    def metabolitos(self):
        """
        Devolve uma lista de todos os metabolitos únicos presentes nas reações.

        """
        todos_metabolitos = set()
        for reacao in self.reactions.values():
            for met in reacao['cons']:
                todos_metabolitos.add(met)
            for met in reacao['prod']:
                todos_metabolitos.add(met)
        return sorted(list(todos_metabolitos))

    def consome(self, react):
        """
        Devolve a lista de metabolitos consumidos por uma reação específica.

        """
        return self.reactions[react]['cons']

    def produz(self, react):
        """
        Devolve a lista de metabolitos produzidos por uma reação específica.

        """
        return self.reactions[react]['prod']

    def consomem(self, met):
        """
        Devolve a lista de reações que consomem um determinado metabolito.

        """
        reacoes = []
        for react, val in self.reactions.items():
            if met in val['cons']:
                reacoes.append(react)
        return reacoes

    def produzem(self, met):
        """
        Devolve a lista de reações que produzem um determinado metabolito.

        """
        reacoes = []
        for react, val in self.reactions.items():
            if met in val['prod']:
                reacoes.append(react)
        return reacoes

    def mlig(self, met):
        """
        Devolve os metabolitos produzidos por reações que consomem um determinado metabolito.

        """
        reacoes_consumidoras = self.consomem(met)
        produtos = set()
        for react in reacoes_consumidoras:
            for prod in self.reactions[react]['prod']:
                produtos.add(prod)
        return sorted(list(produtos))

    def rlig(self, react):
        """
        Devolve as reações que consomem os produtos de uma reação específica.

        """
        produtos = self.produz(react)
        reacoes_consomidoras = set()
        for met in produtos:
            for reac in self.consomem(met):
                reacoes_consomidoras.add(reac)
        return sorted(list(reacoes_consomidoras))

    def ativadas_por(self, *metabolitos):
        """
        Devolve as reações ativadas por um conjunto de metabolitos.
        Uma reação é ativada se todos os seus metabolitos consumidos estiverem no conjunto dado.

        """
        metabolitos_set = set(metabolitos)
        reacoes = []
        for react, val in self.reactions.items():
            if set(val['cons']).issubset(metabolitos_set):
                reacoes.append(react)
        return reacoes

    def produzidos_por(self, *lista_reacoes):
        """
        Devolve todos os metabolitos produzidos por um conjunto de reações.

        """
        produtos = set()
        for react in lista_reacoes:
            for met in self.produz(react):
                produtos.add(met)
        return sorted(list(produtos))

    def m_ativ(self, *metabolitos):
        """
        Devolve todos os metabolitos resultantes de reações ativadas por um conjunto inicial de metabolitos.
        Considera reações adicionais ativadas por produtos intermediários.

        """
        if not metabolitos or not all(isinstance(m, str) for m in metabolitos):
            return []
        metabolitos_ativos = set(metabolitos)
        ativados = set()
        while True:
            novas_reacoes = set(self.r_ativ(*metabolitos_ativos)) - ativados
            if not novas_reacoes:
                break
            ativados.update(novas_reacoes)
            for react in novas_reacoes:
                for met in self.produz(react):
                    metabolitos_ativos.add(met)
        return sorted(list(metabolitos_ativos))

    def r_ativ(self, *metabolitos):
        """
        Devolve todas as reações ativadas (direta ou indiretamente) por um conjunto de metabolitos.

        """
        if not metabolitos or not all(isinstance(m, str) for m in metabolitos):
            return []
        ativadas = set()
        novos_metabolitos = set(metabolitos)
        while True:
            novas_ativadas = set()
            for react, val in self.reactions.items():
                if set(val['cons']).issubset(novos_metabolitos) and react not in ativadas:
                    novas_ativadas.add(react)
            if not novas_ativadas:
                break
            ativadas.update(novas_ativadas)
            for react in novas_ativadas:
                for met in self.produz(react):
                    novos_metabolitos.add(met)
        return sorted(list(ativadas))

    def visualize_network(self):
        """
        Visualiza a rede metabólica como um grafo direcionado, com reações em caixas e metabolitos em elipses.
        Ligações vermelhas indicam consumo e ligações verdes indicam produção.

        """
        dot = Digraph(comment='Metabolic Network')

        for react in self.reactions:
            dot.node(react, react, shape='box', color='lightblue2', style='filled')
            for met in self.reactions[react]['cons']:
                dot.node(met, met, shape='ellipse', color='grey', style='filled')
                dot.edge(met, react, color='red')
            for met in self.reactions[react]['prod']:
                dot.node(met, met, shape='ellipse', color='grey', style='filled')
                dot.edge(react, met, color='green')

        output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'output')
        os.makedirs(output_dir, exist_ok=True)
        dot.render(os.path.join(output_dir, 'metabolic_network.gv'), view=True)
        return dot


if __name__ == "__main__":
    print("[RUNNING TEST 1]")

    reactions_2 = {
        "R_PPPNDO": "M_h_c + M_o2_c + M_pppn_c + M_nadh_c => M_nad_c + M_cechddd_c",
        "R_NTPP7": "M_dttp_c + M_h2o_c => M_ppi_c + M_dtmp_c + M_h_c",
        "R_PDH": "M_nad_c + M_coa_c + M_pyr_c => M_nadh_c + M_accoa_c + M_co2_c",
        "R_IMPC": "M_imp_c + M_h2o_c <=> M_fprica_c",
        "R_METS": "M_5mthf_c + M_hcys_DASH_L_c => M_thf_c + M_met_DASH_L_c",
        "R_DMATT": "M_dmpp_c + M_ipdp_c => M_grdp_c + M_ppi_c",
        "R_RBK": "M_rib_DASH_D_c + M_atp_c => M_r5p_c + M_adp_c + M_h_c",
        "R_NTPP4": "M_ctp_c + M_h2o_c => M_ppi_c + M_cmp_c + M_h_c",
        "R_SERAT": "M_ac_c + M_ser_DASH_L_c => M_coa_c + M_acser_c",
        "R_MECDPS": "M_mecdp_c => M_h2o_c + M_mec_c",
        "R_DHORD_NAD": "M_dhor_S_c + M_nad_c => M_orot_c + M_nadh_c",
        "R_HSK": "M_atp_c + M_hser_DASH_L_c => M_adp_c + M_pi_c + M_phser_c",
        "R_AGPAT160": "M_16_0_c + M_ctp_c + M_g3p_c => M_cmp_c + M_pg160_c",
        "R_FRD4": "M_fum_c + M_q8h2_c => M_succ_c + M_q8_c",
        "R_HMGL": "M_hmgcoa_c => M_acac_c + M_accoa_c",
        "R_GRTT": "M_trnaglu_c + M_glu_DASH_L_c => M_glutrna_c",
        "R_POR5": "M_5prdmbz_c + M_2mbz_c => M_h_c + M_2pp_c",
        "R_PANTS": "M_pnto_R_c + M_atp_c + M_cys_DASH_L_c => M_ppan_c + M_amp_c + M_ppi_c",
        "R_HISTP": "M_31php_c => M_his_DASH_L_c",
        "R_PRFGS": "M_fprica_c + M_glu_DASH_L_c + M_atp_c => M_fgams_c + M_adp_c + M_pi_c",
        "R_DXPRIi": "M_dxp_c => M_dhpt_c",
        "R_G6PDH2r": "M_g6p_c + M_nadp_c <=> M_6pgl_c + M_nadph_c + M_h_c",
        "R_PGL": "M_6pgl_c + M_h2o_c => M_6pgc_c + M_h_c",
        "R_GND": "M_6pgc_c + M_nadp_c => M_ru5p_DASH_D_c + M_nadph_c + M_co2_c",
        "R_RPI": "M_ru5p_DASH_D_c <=> M_r5p_c",
        "R_RPE": "M_ru5p_DASH_D_c <=> M_xu5p_DASH_D_c",
        "R_TKT1": "M_r5p_c + M_xu5p_DASH_D_c <=> M_g3p_c + M_s7p_c",
        "R_TALA": "M_s7p_c + M_g3p_c <=> M_f6p_c + M_ery4p_c",
        "R_TKT2": "M_ery4p_c + M_xu5p_DASH_D_c <=> M_f6p_c + M_g3p_c"
    }

    network2 = MetabolicNetwork(reactions_2)

    def all_betweenness_centrality(g):
        bc = {}
        for node in g.get_nodes():
            bc[node] = g.betweenness_centrality(node)
        return bc
    print("- Distância média e conectividade:", network2.mean_distances())
    print("- Clustering médio:", network2.mean_clustering_coef())

    print("\n- Top 3 nós com maior grau:")
    for no in network2.highest_degrees(top=3):
        print(f"  {no} (grau: {network2.degree(no)})")

    print("\n- Top 3 nós com maior closeness:")
    closeness = {n: network2.closeness_centrality(n) for n in network2.get_nodes()}
    for no, val in sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"  {no}: {val:.4f}")

    print("\n- Top 3 nós com maior betweenness centrality:")
    bc_dict = all_betweenness_centrality(network2)
    for no, val in sorted(bc_dict.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"  {no}: {val:.4f}")

    iniciais = ["M_g6p_c", "M_nadp_c"]
    print("- \n Metabolitos iniciais:", iniciais)
    ativadas = network2.ativadas_por(*iniciais)
    print("- Reações ativadas:", ativadas)
    print("- Metabolitos produzidos por essas reações:", network2.produzidos_por(*ativadas))
    print("- Metabolitos finais possíveis:", network2.m_ativ(*iniciais))
    network2.visualize_network()
