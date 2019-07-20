import pull_and_protein
import build_edition

def main(
    PULL=0,
    VARS="test_vars.yml"
):
    build_config = pull_and_protein.main(
        PULL=PULL,
    )
    open(VARS, w).write(build_config)
    build_edition.main(
        varsfile=VARS
    )


if __name__ == "__main__":
    main(
        PULL=1,
    )
