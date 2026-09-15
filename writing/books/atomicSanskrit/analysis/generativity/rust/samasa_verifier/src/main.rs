use std::io::{self, BufRead};
use serde_json::json;
use vidyut_prakriya::args::{Linga, Pratipadika, Samasa, SamasaType, Slp1String, Subanta, Vacana, Vibhakti};
use vidyut_prakriya::Vyakarana;

fn basic(text: &str) -> Pratipadika {
    Pratipadika::basic(Slp1String::from(text).expect("valid SLP1"))
}

fn nominal(text: &str, vibhakti: Vibhakti) -> Subanta {
    Subanta::new(basic(text), Linga::Pum, vibhakti, Vacana::Eka)
}

fn args(helper: &str, members: &[&str]) -> Samasa {
    let (padas, kind) = match helper {
        "avyayibhava" => (
            vec![Subanta::avyaya(basic(members[0])), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Avyayibhava,
        ),
        "avyaya_tatpurusha" => (
            vec![Subanta::avyaya(basic(members[0])), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Tatpurusha,
        ),
        "dvitiya_tatpurusha" => (
            vec![nominal(members[0], Vibhakti::Dvitiya), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Tatpurusha,
        ),
        "trtiya_tatpurusha" => (
            vec![nominal(members[0], Vibhakti::Trtiya), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Tatpurusha,
        ),
        "caturthi_tatpurusha" => (
            vec![nominal(members[0], Vibhakti::Caturthi), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Tatpurusha,
        ),
        "panchami_tatpurusha" => (
            vec![nominal(members[0], Vibhakti::Panchami), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Tatpurusha,
        ),
        "sasthi_tatpurusha" => (
            vec![nominal(members[0], Vibhakti::Sasthi), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Tatpurusha,
        ),
        "saptami_tatpurusha" => (
            vec![nominal(members[0], Vibhakti::Saptami), nominal(members[1], Vibhakti::Prathama)],
            SamasaType::Tatpurusha,
        ),
        "karmadharaya" => (
            members.iter().map(|x| nominal(x, Vibhakti::Prathama)).collect(),
            SamasaType::Karmadharaya,
        ),
        "bahuvrihi" => (
            members.iter().map(|x| nominal(x, Vibhakti::Prathama)).collect(),
            SamasaType::Bahuvrihi,
        ),
        "dvandva" => (
            members.iter().map(|x| nominal(x, Vibhakti::Prathama)).collect(),
            SamasaType::Dvandva,
        ),
        "samahara_dvandva" => (
            members.iter().map(|x| nominal(x, Vibhakti::Prathama)).collect(),
            SamasaType::SamaharaDvandva,
        ),
        _ => panic!("unknown helper: {helper}"),
    };
    Samasa::builder().padas(padas).samasa_type(kind).build().expect("valid samasa")
}

fn main() {
    let v = Vyakarana::new();
    for line in io::stdin().lock().lines() {
        let line = line.expect("read input");
        let fields: Vec<&str> = line.split('\t').collect();
        if fields.len() != 3 {
            panic!("expected id, helper, members");
        }
        let members: Vec<&str> = fields[2].split(';').collect();
        let mut derivations: Vec<_> = v.derive_samasas(&args(fields[1], &members))
            .iter()
            .map(|p| {
                let path: Vec<_> = p.history().iter().map(|step| {
                    json!({
                        "rule_source": step.rule().source_name(),
                        "rule": step.rule().code(),
                        "result": step.result().iter().map(|term| term.text()).collect::<Vec<_>>().join(" + "),
                    })
                }).collect();
                json!({"form_slp1": p.text(), "path": path})
            })
            .collect();
        derivations.sort_by_key(|x| x["form_slp1"].as_str().unwrap_or("").to_string());
        derivations.dedup_by(|a, b| a["form_slp1"] == b["form_slp1"]);
        println!("{}", json!({
            "id": fields[0],
            "compound_type": fields[1],
            "members_slp1": members,
            "derivations": derivations,
        }));
    }
}
